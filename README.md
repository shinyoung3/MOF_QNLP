## MOF QNLP : Inverse Design of Metal-Organic Frameworks Using Quantum Natural Language Processing

MOF QNLP provides a new experience in constructing MOFs with target properties based on quantum natural language processing (QNLP). The QNLP models were trained to correctly categorize 450 hypothetical MOFs into four distinct classes of pore volume and CO<sub>2</sub> Henry's constant. The overall MOF generation framework is as followed:

1. The user selects target property classes among **Low, Moderately Low, Moderately High, and High** pore volume or CO<sub>2</sub> Henry's constant. 
2. Classical computing-based MOF generation process generates text-based MOF input by randomly selecting MOF building blocks in each MOF component's search space. This MOF input is transformed into quantum circuit, which is the input of QNLP models.
3. Quantum computing-based classification models provide feedback to the MOF generation loop to output MOF with desired properties. 
4. The MOF that meets the threshold probability (85% for pore volume, 65% for CO<sub>2</sub> Henry's constant) goes through the structure generation process, while those that do not are redirected back to step 2.

![MOF generation process](https://github.com/shinyoung3/MOF_QNLP/blob/main/image/MOF_QNLP_process.jpg)


## Usage

The Jupyter notebook files were provided to reproduce our QNLP model training and MOF generation processes. 

- `mof_qnlp_model_training.ipynb` : QNLP model training process
- `mof_generation_example.ipynb` : MOF generation based on hybrid quantum-classical approach
- `mof_qnlp/models` : Contains QNLP models trained over pore volume (`pv`) and CO<sub>2</sub> Henry's constant (`co2_henry`).
- `mof_qnlp/mof_dataset` : MOF QNLP training datasets for pore volume (`pv`) and CO<sub>2</sub> Henry's constant (`co2_henry`).
- `cifs`: Contains the full set of 450 generated MOF structures in Crystallographic Information Framework (.cif) format 



## Citation

If you want to cite MOF QNLP paper, please refer: 

- Inverse Design of Metal-Organic Frameworks Using Quantum Natural Language Processing [[link]](https://arxiv.org/abs/2405.11783)

  



