import numpy as np
import copy

class Genome():

    # static - do not need to create a genome object before it can be used
    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene
    
    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for i in range(gene_count)]
        return genome
    
    @staticmethod
    def get_gene_spec():
        gene_spec = {
            "link-shape" : {"scale": 1},
            "link-length" : {"scale": 1},
            "link-radius" : {"scale": 1},
            "link-recurrence" : {"scale": 4},
            "link-mass" : {"scale": 1},
            "joint-type" : {"scale": 1},
            "joint-parent" : {"scale": 1},
            "joint-axis-xyz" : {"scale": 1},
            "joint-origin-rpy-1" : {"scale": np.pi * 2},
            "joint-origin-rpy-2" : {"scale": np.pi * 2},
            "joint-origin-rpy-3" : {"scale": np.pi * 2},
            "joint-origin-xyz-1" : {"scale": 1},
            "joint-origin-xyz-2" : {"scale": 1},
            "joint-origin-xyz-3" : {"scale": 1},
            "control-waveform" : {"scale": 1},
            "control-amp" : {"scale": 0.25},
            "control-freq" : {"scale": 1}
        }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]['ind'] = ind
            ind += 1
        return gene_spec
    
    @staticmethod
    def get_gene_dict(gene, spec):
        gdict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gdict[key] = gene[ind] * scale
        return gdict
    
    @staticmethod
    def get_genome_dicts(genome, spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene, spec))
        return gdicts
    
    @staticmethod
    def genome_to_links(gdicts):
        link_ind = 0
        parent_names = [str(link_ind)]
        links = []
        for gdict in gdicts:
            link_ind += 1
            link_name = str(link_ind)
            parent_ind = gdict["joint-parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link-recurrence"]
            link = URDFLink(name=link_name,
                            parent_name=parent_name,
                            recur=recur,
                            link_length=gdict["link-length"])
            links.append(link)
            parent_names.append(link_name)
        return links
    
    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        for c in children:
            for r in range(c.recur):
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                exp_links.append(c_copy)
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)
    

class URDFLink:
    def __init__(self, name, parent_name, recur,
                 link_length=0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
