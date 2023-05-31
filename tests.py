from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, kstest

import generators
from pseudorandom import PseudoRandomNumberGenerator


@dataclass
class ChiSquareResult:
    consistent: bool
    chi_square: float
    critical_value: float
    p_value: float


@dataclass
class KolmogorovSmirnovResult:
    consistent: bool
    statistic: float
    p_value: float


class PseudoRandomTests:
    def _get_generators(self):
        return generators.__all__

    def generate(
        self,
        generator_class: PseudoRandomNumberGenerator,
        seed: int,
        amount: int,
        output_path: str,
    ) -> list[float]:
        path = Path(output_path)
        generator = generator_class()
        generator.seed(seed)

        numbers = [generator.uniform() for _ in range(amount)]

        path.parent.mkdir(exist_ok=True)
        with open(output_path, "w") as output_file:
            output_file.write("\n".join([str(number) for number in numbers]))

        return numbers

    def chi_square_uniformity_test(
        self, samples: list[float]
    ) -> ChiSquareResult:
        """
        Performs the chi-square test for uniformity on a given list of samples.

        :param samples: A list of samples.
        :type samples: list[float]
        :return: A tuple containing the test result,
        chi-square value, critical value, and p-value.
        :rtype: ChiSquareResult

        The test result is a ChiSquareResult dataclass with:
            - boolean indicating if the null hypothesis
            is accepted (True) or rejected (False).
            - The chi-square value represents the test statistic.
            - The critical value is the threshold value
            for accepting or rejecting the null hypothesis.
            - The p-value is the probability of observing
            the test statistic or a more extreme value.
        """
        bins = len(samples) // 100

        expected_frequency = len(samples) / bins
        observed_frequency, _ = np.histogram(samples, bins=bins)

        chi_square = np.sum(
            (observed_frequency - expected_frequency) ** 2 / expected_frequency
        )
        critical_value = chi2.ppf(0.95, bins - 1)
        p_value = 1 - chi2.cdf(chi_square, bins - 1)

        return ChiSquareResult(
            chi_square <= critical_value,
            chi_square,
            critical_value,
            p_value,
        )

    def kolmogorov_smirnov_test(
        self, samples: list[float], dist: str = "uniform"
    ) -> KolmogorovSmirnovResult:
        """
        Performs the Kolmogorov-Smirnov test on a given list of samples.

        :param samples: A list of samples.
        :type samples: list[float]
        :param dist: The distribution to compare against.
        Defaults to "uniform".
        :type dist: str, optional
        :return: A tuple containing the test result,
        test statistic, and p-value.
        :rtype: KolmogorovSmirnovResult

        The test result is a KolmogorovSmirnovResult dataclass with:
            - boolean indicating if the null hypothesis
            is accepted (True) or rejected (False).
            - The test statistic represents the maximum distance
            between the empirical distribution function
            of the samples and the specified distribution.
            - The p-value is the probability of observing
            the test statistic or a more extreme value.

        """
        statistic, p_value = kstest(samples, dist)
        return KolmogorovSmirnovResult(p_value > 0.05, statistic, p_value)

    def plot_p_values(
        self, test_names: list[str], p_values: list[float], save_path: str
    ):
        """
        Creates a bar chart to visualize the p-values
        and saves it as an image file.

        :param test_names: A list of test names.
        :param p_values: A list of p-values.
        :param save_path: The file path to save the chart.
        """

        # Set up the figure and axes
        fig, ax = plt.subplots()

        # Create the bar chart for p-values
        x = range(len(test_names))
        width = 0.35
        ax.bar(x, p_values, width, color="#6940A5")

        # Add labels, title, and legend
        ax.set_xlabel("Test")
        ax.set_ylabel("P-Value")
        ax.set_title("P-Values")
        ax.set_xticks(x)
        ax.set_xticklabels(test_names)

        path = Path(save_path)
        path.parent.mkdir(exist_ok=True)

        plt.savefig(save_path)

    def plot_chi_square_values(
        self,
        test_names: list[str],
        chi_square_values: list[float],
        save_path: str,
    ):
        """
        Creates a bar chart to visualize the chi-square values and
        saves it as an image file.

        :param test_names: A list of test names.
        :param chi_square_values: A list of chi-square values.
        :param save_path: The file path to save the chart.
        """

        # Set up the figure and axes
        fig, ax = plt.subplots()

        # Create the bar chart for chi-square values
        x = range(len(test_names))
        width = 0.35
        ax.bar(x, chi_square_values, width, color="#AD1A72")

        # Add labels, title, and legend
        ax.set_xlabel("Test")
        ax.set_ylabel("Chi-Square Value")
        ax.set_title("Chi-Square Values")
        ax.set_xticks(x)
        ax.set_xticklabels(test_names)

        path = Path(save_path)
        path.parent.mkdir(exist_ok=True)

        plt.savefig(save_path)

    def plot_number_sequences(
        self,
        test_names: list[str],
        number_sequences: list[list[float]],
        save_path: str,
    ):
        """
        Creates a line plot to visualize the number sequences
        and saves it as an image file.

        :param test_names: A list of test names.
        :param number_sequences: A list of number sequences.
        :param save_path: The file path to save the chart.
        """

        _, ax = plt.subplots()

        for i, numbers in enumerate(number_sequences):
            mu = np.mean(numbers)
            sigma = np.std(numbers)
            x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
            y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
                -((x - mu) ** 2) / (2 * sigma**2)
            )

            plt.plot(x, y, alpha=0.5, label=test_names[i])

        plt.xlabel("x")
        plt.ylabel("Probability density")
        plt.title("Normal Distribution")
        ax.legend()

        path = Path(save_path)
        path.parent.mkdir(exist_ok=True)

        plt.savefig(save_path)

    def run(self, seed: int = None):
        generators = self._get_generators()

        # Doing this to prevent seed == 0 (breaks XORShift)
        seed = seed or 0
        while seed == 0:
            seed = int(datetime.now().timestamp()) % 100000

        print(" Seed:", seed)

        names = []
        chi_square_values = []
        p_values = []
        sequences = []

        output = f"Seed: {seed}\n\n"
        for generator in generators:
            numbers = self.generate(
                generator, seed, 10000, f"out/{generator.__name__}.txt"
            )

            chi_test = self.chi_square_uniformity_test(numbers)
            ks_test = self.kolmogorov_smirnov_test(numbers)

            names.append(generator.__name__)
            chi_square_values.append(chi_test.chi_square)
            p_values.append(chi_test.p_value)
            sequences.append(numbers[:100])

            output += "\n".join(
                [
                    f"[ {generator.__name__} ]",
                    "\n[TEST] > Chi Square",
                    f"         P value        : {chi_test.p_value}",
                    f"         Chi-square     : {chi_test.chi_square}",
                    f"         Critical value : {chi_test.critical_value}",
                    "The distribution is"
                    f"{' ' if chi_test.consistent else ' not '}"
                    "consistent with the specified distribution.",
                    "\n[TEST] > Kolmogorov Smirnov",
                    f"         P value        : {ks_test.p_value}",
                    f"         Statistic      : {ks_test.statistic}",
                    "The distribution is"
                    f"{' ' if ks_test.consistent else ' not '}"
                    "consistent with the specified distribution.\n\n",
                ]
            )

        print(output)

        with open("out/test.txt", "w") as out:
            out.write(output)

        self.plot_p_values(names, p_values, "out/p_values.png")
        self.plot_chi_square_values(
            names, chi_square_values, "out/chi_values.png"
        )
        self.plot_number_sequences(names, sequences, "out/numbers.png")


PseudoRandomTests().run()
