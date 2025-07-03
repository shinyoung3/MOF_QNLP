from pathlib import Path
from lambeq import TketModel, spiders_reader, AtomicType, IQPAnsatz
from pytket.extensions.qiskit import AerBackend
import random
import numpy as np

backend = AerBackend()
backend_config = {
    'backend': backend,
    'compilation': backend.default_compilation_pass(2),
    'shots': 8192
}

property_to_model = {
    "low": "q1",
    "mod low": "q2",
    "mod high": "q3",
    "high": "q4"
}
model_names = ["q1", "q2", "q3", "q4"]

def generate_mof(target_class, target_property, max_iterations=100):
    """
    Generate a MOF string with desired property and class using QNLP classifiers.
    Args:
        target_class (str): "low", "mod low", "mod high", "high"
        target_property (str): "pore volume" or "co2 henry's constant"
        max_iterations (int): number of attempts to find suitable MOF

    Returns:
        None. Prints the result.
    """
    # Set all file paths and threshold according to property
    if target_property.lower() == "pore volume":
        model_dir = Path('/home/young33/qnlg/for_submit/MOF_QNLP/mof_qnlp/models/pv')
        data_dir = Path("/home/young33/qnlg/for_submit/MOF_QNLP/mof_qnlp/dataset/pv/20_80")
        file_template = 'pv_multi_{model_name}.txt'
        confidence_threshold = 0.85
    elif target_property.lower() in ["co2 henry's constant", "co2 henrys constant"]:
        model_dir = Path('/home/young33/qnlg/for_submit/MOF_QNLP/mof_qnlp/models/co2_henry')
        data_dir = Path("/home/young33/qnlg/for_submit/MOF_QNLP/mof_qnlp/dataset/co2_henry/20_80")
        file_template = 'log_henry_multi_{model_name}.txt'
        confidence_threshold = 0.65
    else:
        raise ValueError("Unknown target_property. Use 'pore volume' or 'co2 henry's constant'.")

    # Helper to load the model for a property
    def load_model(model_name):
        model_folder = model_dir / f'{model_name}'
        model_path = next(model_folder.glob('*.lt'))
        model = TketModel(backend_config=backend_config)
        model.load(str(model_path))
        return model

    # Helper to read true labels for a model
    def read_true_labels(model_name):
        file_path = data_dir / f'{model_name}' / file_template.format(model_name=model_name)
        true_labels = {}
        with open(file_path, 'r') as file:
            for line in file:
                label, *mof_name = line.strip().split()
                mof_name = " ".join(mof_name)
                true_labels[mof_name] = label
        return true_labels

    # Quantum circuit prediction
    def _measure_quantum_circuit_for_mof(model, mof_name):
        diagram = spiders_reader.sentences2diagrams([mof_name])
        ansatz = IQPAnsatz({AtomicType.NOUN: 0, AtomicType.SENTENCE: 1}, n_layers=1, n_single_qubit_params=3)
        circuit = [ansatz(d) for d in diagram]
        prediction_probs = model.get_diagram_output(circuit)[0]
        return prediction_probs

    # Main search loop
    target_model = property_to_model[target_class]
    iteration = 0
    final_mof_name = None
    final_result = None

    while iteration < max_iterations:
        from mof_qnlp import create_mof_search_space
        mofs = create_mof_search_space()
        mof_name = " ".join(random.choice(mofs))
        print(f"Iteration {iteration + 1}: Evaluating MOF: {mof_name} for target class: {target_class}, property: {target_property}")

        model_predictions = {}
        for model_name in model_names:
            model = load_model(model_name)
            prediction_probs = _measure_quantum_circuit_for_mof(model, mof_name)
            model_predictions[model_name] = prediction_probs

        total_prob_label_0 = sum(probs[0] for probs in model_predictions.values())
        relative_probs = {model: probs[0] / total_prob_label_0 for model, probs in model_predictions.items()}

        # Find best property prediction by model
        best_model = max(relative_probs, key=relative_probs.get)
        best_relative_prob = relative_probs[best_model]
        predicted_class = next(key for key, value in property_to_model.items() if value == best_model)

        for model_name, probs in model_predictions.items():
            print(f"{model_name}: Prediction Probs: {probs}, Relative Prob Label 0: {relative_probs[model_name]:.3f}")

        if predicted_class == target_class and best_relative_prob > confidence_threshold:
            best_label = 0 if model_predictions[best_model][0] > model_predictions[best_model][1] else 1
            true_labels = read_true_labels(best_model)
            true_label = true_labels.get(mof_name, "unknown")
            correctness = "correct" if str(best_label) == true_label else "incorrect"
            final_mof_name = mof_name
            final_result = (best_model, predicted_class, best_label, true_label, correctness)
            print(f"Best Model: {best_model}, Predicted Class: {predicted_class}, Predicted Label: {best_label}, True Label: {true_label}, Correctness: {correctness}")
            break

        iteration += 1

    if final_mof_name:
        print(f"\nThe final MOF structure with desired property is: {final_mof_name}")
        return {
            "mof_name": final_mof_name,
            "best_model": best_model,
            "predicted_class": predicted_class,
            "best_label": best_label,
            "true_label": true_label,
            "correctness": correctness
        }

    else:
        print("Max iterations reached without matching target class/property")
        return None
