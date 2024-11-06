import numpy as np
import unittest

# generate random data
def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

# calculate aggregated threat score
def calculate_aggregated_threat_score(department_scores, importance_scores):
    total_weighted_score = 0
    total_importance = sum(importance_scores)

    # weighted average threat score
    for score, importance in zip(department_scores, importance_scores):
        department_average = np.mean(score)
        weighted_score = department_average * importance
        total_weighted_score += weighted_score

    aggregated_score = total_weighted_score / total_importance
    return min(max(aggregated_score, 0), 90)

# example
departments = {
    'Engineering': generate_random_data(30, 10, 100),
    'Marketing': generate_random_data(50, 20, 150),
    'Finance': generate_random_data(40, 15, 120),
    'HR': generate_random_data(20, 5, 60),
    'Science': generate_random_data(70, 10, 80)
}
importance_tags = [3, 4, 5, 2, 1]
department_scores = list(departments.values())
aggregated_score = calculate_aggregated_threat_score(department_scores, importance_tags)
print(f"Aggregated User Threat Score: {aggregated_score}")


class TestAggregatedThreatScore(unittest.TestCase):

    def test_no_threats(self):
        # test case where all scores are zero
        scores = [generate_random_data(0, 0, 100) for _ in range(5)]
        importance = [1, 1, 1, 1, 1]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertEqual(result, 0)

    def test_high_threat_in_important_department(self):
        # test case where one important department has high threats
        scores = [generate_random_data(20, 5, 100) for _ in range(4)]
        scores.append(generate_random_data(80, 5, 100))  # High threat department
        importance = [1, 1, 1, 1, 5]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertGreater(result, 50)  # Expect higher score due to one critical department

    def test_uniform_scores_different_importance(self):
        # test case with similar scores but different importances
        scores = [generate_random_data(45, 5, 100) for _ in range(5)]
        importance = [1, 2, 3, 4, 5]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertAlmostEqual(result, 45, delta=5)  # expect result close to 45 due to uniform threats

    def test_large_variance(self):
        # test with a wide variance in threat scores across departments
        scores = [generate_random_data(10, 20, 150), generate_random_data(60, 10, 80),
                  generate_random_data(30, 15, 50), generate_random_data(80, 5, 200),
                  generate_random_data(5, 10, 100)]
        importance = [1, 2, 1, 3, 1]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertTrue(0 <= result <= 90)

    def test_all_high_threats_same_importance(self):
        # all departments with high scores, equal importance
        scores = [generate_random_data(85, 2, 100) for _ in range(5)]
        importance = [3, 3, 3, 3, 3]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertGreater(result, 80)

    def test_varying_department_size(self):
        # test case with varying number of users per department
        scores = [generate_random_data(20, 5, 10), generate_random_data(60, 10, 50),
                  generate_random_data(30, 15, 200), generate_random_data(10, 5, 150),
                  generate_random_data(70, 5, 30)]
        importance = [1, 3, 2, 4, 5]
        result = calculate_aggregated_threat_score(scores, importance)
        self.assertTrue(0 <= result <= 90)

if __name__ == "__main__":
    unittest.main()
