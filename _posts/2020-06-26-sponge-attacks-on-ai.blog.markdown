---
layout: post
title:  "Sponge Example Attacks On Deep Neural Networks"
date:   2016-07-08 22:05:59 +0200
categories: infosec ai
---

_Is there a significant gap in energy consumption [of Deep Neural Networks] for different inputs of the same dimension? Put another way, can you drain the batteries of an embedded device if it uses artificial intelligence?_ This question motivated [recent research by Ilia Shumailov et al](https://arxiv.org/pdf/2006.03463.pdf), scientists at the Cambridge University and the University of Toronto. Surprisingly, the researchers discovered that different inputs of the same size can cause a Deep Neural Network (DNN) to draw very different amounts of time and energy.

# The Energy Gap
According to the researchers, the amount of energy consumed by one inference pass of a DNN (i.e., a forward pass in a neural network) mainly depends on:

* the number of arithmetic operations and
* the number of memory access operations

needed to process the input. Based on that, Shumailov et al hypothesized that DNNs might have a large energy gap between different inputs because inputs that:

* lead to less sparse activations and
* lead to significant changes in the internal representation size during the DNN computation 

increase the number of operations and the number of memory accesses. As a result, the researchers proposed a method for constructing DNN inputs that lead to abnormally high energy consumption.

# The Attack
Typically, one cares about the average-case performance of machine learning models. Shumailov and his fellow researchers, in contrast, investigated how different inputs of the same size affect the power consumption and the computation time (i.e., the latency) of DNNs. In the process, they found that specially crafted inputs can increase the energy consumption of DNNs by a factor of 10 to 200. The same holds for the latency of the DNNs. This observation builds the basis of the new attack that increases the power drawn by neural networks and the time they take to make decisions.

In addition, the researchers showed that the malicious inputs are _portable_. In other words, the same inputs lead to increased power consumption and latency across different CPUs and a variety of hardware accelerators including GPUs and ASICs.

# How Does the Attack Work?
The researchers actually introduced two variants of the attack. The first variant uses a genetic algorithm to craft malicious inputs which the authors refer to _sponge examples_ as these inputs are specifically designed to soak up energy from a neural network. The fitness function for the genetic algorithm is based on the time measurements for the mutated inputs. The name of the malicious inputs - "sponge examples" - is obviously a hommage to widely known ["adversarial examples"](https://arxiv.org/pdf/1412.6572.pdf), inputs formed by applying small but intentionally worst-case perturbations to examples from the dataset, such that the perturbed input results in the model outputting an incorrect answer with high confidence.

The second attack variant optimizes the sponge examples using [L-BFGS](https://en.wikipedia.org/wiki/Limited-memory_BFGS), an optimization algorithm widely used for parameter estimation in machine learning. The loss function makes the optimizer return inputs with large activation norms across all hidden layers of a neural network.

# How Dangerous is the Attack?
Shumailov et al evaluated their sponge examples on numerous popular DNNs for Natural Language Processing (NLP) and Computer Vision (CV). For NLP, the researchers were able to construct sponge examples that slowed down the DNNs by a factor of up to 70 and increased their power consumption by a factor of up to 157. According to Shumailov et al, the main reason for the performance degradation was the increased computation dimension.

An interesting observation made by Shumailov et al for NLP DNNs is that the sample inputs from the evaluation set (i.e., typical natural language samples) consume a lot less energy than random noise. The researchers conclude that this can be attributed to the fact that natural samples are efficiently encoded, whereas random produce an unnecessarily long representation. This, in turn, means that random noise can be used as a scalable attack vector in a black-box scenario (i.e., where the attacker does not know the internal implementation details of a DNN).

For CV DNNs, the reported results suggest that sponge examples are marginally more expensive in terms of energy. Concretely, Shumailov et al report a 1 to 3% increase in energy consumption when compared to natural samples (i.e., to the evaluation set with standard images).

# How to Defend Against Sponge Examples?
[In their paper](https://arxiv.org/pdf/2006.03463.pdf), Shumailov et al propose a simple, yet effective defense strategy based on the worst-case analysis of the DNN's energy consumption. Specifically, the researchers propose to profile the DNN's time or energy cost of inference for natural (i.e., benign) examples prior to the DNN's deployment and then fix a _cut-off_ threshold. During operation, this threshold can then be used to control the maximum energy consumption per inference run, thereby mitigating the effect of sponge examples on the availability (i.e., limit sponge examples' potential to drain the battery).

If the threat is the decrease of the DNNs performance, the researchers say that to protect such a system against sponge examples, the system needs to be designed assuming the worst case performance of the DNN and, optionally, by including a fallback mechanism.