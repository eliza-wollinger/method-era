# Modal Estimation with Eigensystem Realization Algorithm (ERA)

Modal estimation is a fundamental aspect of structural dynamics analysis, aimed at determining crucial parameters of structures, including their natural frequencies, damping characteristics, and mode shapes. Among the various methodologies available for modal parameter identification, the Eigensystem Realization Algorithm (ERA) is widely recognized as a powerful and accurate tool. This README serves as a guide to understanding and utilizing ERA for modal parameter identification, particularly in situations involving different levels of viscous damping.

# About Eigensystem Realization Algorithm (ERA)

The Eigensystem Realization Algorithm (ERA) is a state-of-the-art technique for modal parameter identification. ERA excels at extracting key characteristics of a structural system from a set of measured Impulse Response Functions (IRF) data. These IRF data are typically acquired through experimental testing or numerical simulations.

ERA operates by fitting a minimal state-space representation to the IRF data, subsequently solving an eigenvalue problem associated with the state matrix to extract modal parameters. The output of ERA includes the natural frequencies, damping factors, and mode shapes of the structure under consideration.

# Challenges with Viscous Damping

Modal parameter identification is most accurate when dealing with lightly damped systems. However, many real-world structural systems exhibit various levels of viscous damping, which can complicate the process. Viscous damping models, such as proportional and non-proportional damping, are commonly used to describe the energy dissipation in structural systems undergoing vibrational analysis.

The presence of viscous damping introduces challenges in accurately estimating modal parameters. Viscous damping can lead to inaccuracies in the identified natural frequencies, damping ratios, and mode shapes, making it critical to assess and address its impact.

# Objectives of this Article

This article explores the capabilities of ERA in extracting modal parameters from structural systems when varying levels of viscous damping are present. To achieve this, we use Impulse Response Functions (IRF) data obtained through numerical simulations from a five degrees of freedom mechanical system. Additionally, the article investigates the effects of noise in IRF signals, which is often encountered in real-world data acquisition scenarios.

# Getting Started

To make use of ERA for modal parameter identification in the presence of viscous damping, you will need Python and specific packages. Ensure you have the following tools ready:

- Python

## Installation and Usage
Please refer to the accompanying documentation or instructions (if available) to set up and utilize ERA for your specific needs.

## Acknowledgments

I would like to express my heartfelt gratitude to my esteemed advisors, Dr. Heraldo Cambraia and Dr. João Morais da Silva Neto, for their unwavering support, guidance, and mentorship. Their expertise, dedication, and invaluable insights have played a pivotal role in shaping  research.

I'm honored to have had the privilege of working under your mentorship, and I sincerely thank you for your continued belief in my potential. Your contributions to my academic and professional development will forever be cherished.

## License

This project is licensed under the MIT License.
