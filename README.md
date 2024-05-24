## MOF QNLP : Inverse Design of Metal-Organic Frameworks Using Quantum Natural Language Processing

MOF QNLP provides a new experience in constructing MOFs with target properties based on quantum natural language processing (QNLP). The QNLP models were trained to correctly categorize 150 hypothetical MOFs into four distinct classes of pore volume and H<sub>2</sub> uptake. The overall MOF generation framework is as followed:

1. The user selects target property classes among **Low, Moderately Low, Moderately High, and High** pore volume or H<sub>2</sub> uptake. 
2. Classical computing-based MOF generation process generates text-based MOF input by randomly selecting MOF building blocks in each MOF component's search space. This MOF input is transformed into quantum circuit, which is the input of QNLP models.
3. Quantum computing-based classification models provide feedback to the MOF generation loop to output MOF with desired properties. 
4. The MOF that meets the threshold probability of 85% goes through the structure generation process, while those that do not are redirected back to step 2.

![MOF generation process](.\image\MOF_QNLP_process.jpg)



## Usage

The Jupyter notebook files were provided to reproduce our QNLP model training and MOF generation processes. 

- `mof_qnlp_model.ipynb` : QNLP model training process
- `mof_generation.ipynb` : MOF generation based on hybrid quantum-classical approach
- `models` : Contains QNLP models trained over pore volume (`pv`) and H<sub>2</sub> uptake (`h2_uptake`).
- `mof_dataset` : MOF QNLP training datasets for pore volume (`pv`) and H<sub>2</sub> uptake (`h2_uptake`).



## Citation

If you want to cite MOF QNLP paper, please refer: 

- Inverse Design of Metal-Organic Frameworks Using Quantum Natural Language Processing [[link]](https://arxiv.org/abs/2405.11783)

  



