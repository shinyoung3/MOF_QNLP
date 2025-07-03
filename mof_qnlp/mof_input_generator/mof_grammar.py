# Code of this cell from https://github.com/AminKaramlou/QNLG
from nltk import CFG
from nltk.parse.generate import generate

def create_mof_search_space():
    MOF_GRAMMAR = """
      S -> NP VP
      VP -> V 
      NP -> A N
      A -> 'pcu' | 'kag' | 'lcy' 
      N -> 'N106' | 'N123' | 'N139' | 'N144' | 'N155' | 'N173' | 'N205' | 'N248' | 'N394' | 'N505'  
      V -> 'E1' |'E8' | 'E9' | 'E14' | 'E15' | 'E28' | 'E35' | 'E59' | 'E70'  | 'E161' | 'E183' | 'E191' |'E220' | 'E225' | 'E229'  
      """

    VOCAB = ['pcu', 'kag', 'lcy',
             'N106', 'N123', 'N139', 'N144', 
             'N248', 'N394', 'N155',  'N173', 'N205', 
             'N505', 'E14', 'E70', 'E220', 'E15', 
             'E8', 'E35', 'E183', 'E191', 'E1', 
             'E9', 'E28', 'E59', 'E161', 'E225', 
             'E229']

    topology = ['pcu', 'kag', 'lcy']
    building_blocks = ['N106', 'N123', 'N139', 'N144', 'N155', 'N173', 'N205', 'N248', 'N394','N505']

    GRAMMAR = CFG.fromstring(MOF_GRAMMAR)
    MOF = list(generate(GRAMMAR))

    def filter_sentence(mofs):
        # Make sure no MOF appears more than once:
        if not len(set(mofs)) == len(mofs):
            return False

        # Make sure topology appears before node and edge:
        try:
            topo_position = next(i for i,v in enumerate(mofs) if v in topology)
            bb_position = next(i for i,v in enumerate(mofs) if v in building_blocks)
        except:
            return False
        return topo_position < bb_position

    MOF = list(filter(filter_sentence, MOF))
    return MOF