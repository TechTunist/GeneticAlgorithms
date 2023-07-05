import unittest
import genome
import numpy as np


class GenomeTest(unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneIsNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(10))

    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertIsNotNone(gene[0])

    def testRandomGeneHasTenValues(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertEqual(len(gene), 10)

    def testRandGeneIsNumpyArray(self):
        gene = genome.Genome.get_random_gene(10)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(10, 5)
        self.assertIsNotNone(data)

    def testGeneSpecExists(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def testGeneSpecLinkLengthHasIndex(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']["ind"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)

    def testFlatLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1)
        ]
        exp_links = [links[0]]
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links)
        names = [l.name+"-parent-is-"+l.parent_name for l in exp_links]
        print(names)
        self.assertEqual(len(exp_links), 6)

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-recurrence", gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links), 3)
        

    


unittest.main()