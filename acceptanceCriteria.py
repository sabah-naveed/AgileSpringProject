class TestMyCode(unittest.TestCase):
    def test_file_reading(self):
        expected_contents = "+------+-----------------+--------+-------------+-----+-------+-------+----------+----------+\n|  ID  |       Name      | Gender |   Birthday  | Age | Alive | Death |  Child   |  Spouse  |\n+------+-----------------+--------+-------------+-----+-------+-------+----------+----------+\n| @I1@ | Parul /Mahajan/ |   F    | 24 SEP 1995 |  28 |  True |  N/A  | {'@F1@'} |   N/A    |\n| @I2@ |  Pavan /Gupta/  |   M    | 17 MAR 1964 |  59 |  True |  N/A  |   N/A    | {'@F1@'} |\n| @I3@ |  Nisha /Gupta/  |   F    | 30 NOV 1969 |  54 |  True |  N/A  |   N/A    | {'@F1@'} |\n+------+-----------------+--------+-------------+-----+-------+-------+----------+----------+\n+------+---------+----------+------------+---------------+---------+---------------+----------+\n|  ID  | Married | Divorced | Husband ID |  Husband Name | Wife ID |   Wife Name   | Children |\n+------+---------+----------+------------+---------------+---------+---------------+----------+\n| @F1@ |   N/A   |   N/A    |    @I2@    | Pavan /Gupta/ |   @I3@  | Nisha /Gupta/ | {'@I1@'} |\n+------+---------+----------+------------+---------------+---------+---------------+----------+\nIndividuals that are less than 150 years old\n['@I1@', '@I2@', '@I3@']\nIndividuals that have passed away\n[]"
        contents = str(x) + str(y) + lessThan150 + dead

        self.assertEqual(contents, expected_contents)


if __name__ == '__main__':
    unittest.main()