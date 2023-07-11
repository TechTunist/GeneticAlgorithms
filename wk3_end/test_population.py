import unittest
import population

class TestPop(unittest.TestCase):
    def testPopExists(self):
        pop = population.Population(pop_size=10, gene_count=4)
        self.assertIsNotNone(pop)

    def testPopHasIndis(self):
        pop = population.Population(pop_size=10, gene_count=4)
        self.assertEqual(len(pop.creatures), 10)

unittest.main()