---
layout: post
title:  "Benford's Law"
date:   2021-04-09 22:18:23 +0200
categories: jekyll update
---
One of the [Impractical Python Projects](https://nostarch.com/impracticalpythonprojects) in Lee Vaughan's amazing book explores a concept known as the [Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law). This law states that in any list of numbers taken from an arbitrary set of naturally occuring data, more numbers will tend to begin with "1" than with any other digit, and the leading digit is likely to be small.

## A Little Bit of History

In 1881, the Canadian–American astronomer and applied mathematician [Simon Newcomb](https://en.wikipedia.org/wiki/Simon_Newcomb) observed that the pages in front of logarithm books &mdash; that is, pages with the lower page numbers &mdash; were far more worn than those in the back. This observation led him to formulate the hypothesis (which was later proven by other mathematicians) that in any list of measurements, the leading digits are much more likely to be small than large. 

Newcomb's discovery apparently was forgotten and was noted again by a physicist [Frank Benford](https://en.wikipedia.org/wiki/Frank_Benford) who used over 20,000 samples of real-world numbers including measurements of rivers, sizes of US polulations, physical constants, molecular weights, entries from a mathematical handbok, street addresses and numbers contained in _Reader's Digest_ magazine to verify it. Benford published his results in a 1938 paper titled "The Law of Anomalous Numbers". Following the publication, Newcomb's discovery came to be known as _Benford's law_, the _law of anomalous numbers_ or simply the _first-digit law_.

## A Little Bit of Math
From the mathematical point of view, Benford's law is an observation about the frequency distribution of leading digits in many real-life sets of numerical data. It states that in many real-world collections of numbers, the distribution is predictable and _non_-uniform. As an example, the number 1 appears as the leading significant digit about 30% of the time, while 9 appears as the leading significant digit less than 5% of the time. This is very counterintuitive, since most of us would expect a uniform distribution when looking at naturally occurring collections of numbers such as death rates, lenghts of rivers or physical and mathematical constants. As a result, Benford's law is a simple yet very useful tool for fraud detection, e.g., in financial, scientific, and election data.

# Coding Benford's Law
To implement Benford's law, we need 4 basic ingredients:
* Benford's distribution for the leading digits,
* a routine for counting the first digits of a given data set,
* a routine to compute the expected distribution for the first digit for a data set of the given size and
* the Chi-Square test.

In case you want to play around with the code, go to the [Jupyter Notebook](https://colab.research.google.com/drive/1rdRYyH-oEJ9eAGhX2--CY1Y6mtcAtenM?usp=sharing) of this post.

## Benford's Distribution

A set of numbers is said to satisfy the Benford's law if the leading digit satisfies [this distribution](https://en.wikipedia.org/wiki/Benford's_law#Definition). We can use a simple array to hold the probabilities (expressed as percentage) for the corresponding digits 0 to 9.

```python
import sys
import math
from collections import defaultdict
import matplotlib.pyplot as plt

# Benford's law percentages for leading digits 1-9
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
```

## Counting First Digits
Next, we'll need a function to count the frequencies of the first digits in a given data set. In Python, we can use a dictionary to store the count of each digit 0 to 9.

```python
def count_first_digits(data_list):
  """Counts 1st digits in a list of numbers. Returns counts & frequency."""
  first_digits = defaultdict(int) # default value of int is 0
 
  for sample in data_list:
    if sample == '':
      continue
    try:
      int(sample)
    except ValueError as e:
      print("Samples must be integers. Exiting")
      sys.exit(1)
    first_digits[sample[0]] += 1
  
  data_count = [v for (k,v) in sorted(first_digits.items())]
  total_count = sum(data_count)
  data_pct = [(i/total_count) * 100 for i in data_count]
  return data_count, data_pct, total_count
```

The above function takes a list of numbers `data_list` and returns a tuple consisting of:
* frequencies of the first digits 0 to 9 (in other words, the distribution of first digits in the given data set) 
* frequencies of the first digits as percentage
* total count of the fist digits (in other words, the size of the given data set)

Note that it expects the list to contain numbers encoded as strings, for example `['123', '456', ...]`, not as integers (not `[123, 456, ...]`) .

##  Computing the Expected Distribution for First Digits
In addition to counting the frequencies of first digits, we need a function to compute the _expected_ first digit distribution. We can use the Benford's distribution defined above to compute this:

```python
def get_expected_counts(total_count):
  """Return a list of expected Benford's law counts for a total sample count."""
  return [round(p * total_count/ 100) for p in BENFORD]
```

## Performing a Statistical Testing
To find out whether a given list of numbers follows Bendford's law, we'll use a statistical method called [Pearson's Chi-Square test](https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test). Among other things, it can be used as a goodness-of-fit test to determine whether an observed frequency distribution differs from a theoretical distribution. In a nutshell, the goodness-of-fit test works like this. First, you need to compute the test statistic as

$$\chi ^2 = \sum_{i=1}^n \frac{(O_i - E_i)^2}{E_i}$$

In the above formula, $O_i$s denote the observed frequency count and $E_i$s denote the expected frequency count for the first digits 0 to 9. The term $(O_i - E_i)^2$ in the numerator is the deviation between the observed and the expected values. The $E_i$ in denominator norms that deviation. In that sense,  the $\chi ^2$ test statistic resembles a normalized sum of squared deviations between observed and theoretical frequencies.

Next, you determine the degrees of freedom of the statistic and select the desired level of confidence, the $p$-balue, for the test result. For Benford's law, the degrees of freedom is 8 and a typical $p$-value is 0.05.  

Now you need to compare the $\chi^2$ value obtained in step 1 to the critical value from the chi-squared distribution with the same degrees of freedom and the selected confidence level. The latter can also be obtained from [tables like this one](https://web.ma.utexas.edu/users/davis/375/popecol/tables/chisq.html).

If the test statistic exceeds the critical value from the chi-squared distribution, you reject the hypothesis that the observed and the expected distributions are the same. In our specific case, you reject the hypothesis that the given list of numbers follows Benford's law -- you have successfully detected a fraud.

```python
def chi_square_test(data_count, expected_counts):
  """Return boolean on chi-square test (8 DOF & P-val=0.05)."""
  chi_square_stat = 0; # chi-square test statistic
  for data, expected in zip(data_count, expected_counts):
    chi_square = math.pow(data - expected, 2)
    chi_square_stat += chi_square / expected

  print("\nChi Squared Test Statistic = {:.3f}".format(chi_square_stat))
  print("Critical value at P-value of 0.05 is 15.51")

  return chi_square_stat < 15.51
```

The above function takes frequencies of first digits in the given data set (`data_set` argument; equivalent to the observed distribution) and the expected first digit frequencies (`expected_counts`; equivalent to the expected distribution). The `for` loop computes the $\chi ^2$ test statistic. For 8 degrees of freedom and the $p$-value of 0.05, the critical value from the chi-squared distribution is 15.51. The function therefore return `False` whenever the computed test statistic is larger then 15.51.

# Experimenting with Benford's Law
Now that we have all the necessary functions in place, we can play around with Benford's law. First, let's take a dummy dataset that does not follow Benford's law and see if our code detects that.

```python
# Dummy data set to test Benford's law. The most frequent first digit is 4,
# other digits are distributed roughly equally. So the test should return
# 'False', i.e., that the given data is not distributed according to Benford's
# law.
data = ['10', '12', '14', '18', '18', '19', '20', '20', '22', '24', '26', '26', 
        '33', '34', '35', '39', '40', '41', '41', '42', '42', '44', '46', '47', 
        '48', '48', '49', '49', '51', '54', '55', '55', '55', '57', '57', '61', 
        '62', '64', '67', '68', '68', '72', '73', '74', '75', '77', '77', '78',
        '81', '82', '83', '87', '89', '90', '91', '92', '93', '94', '95', '96']


res = count_first_digits(data)
chi_square_test(res[0], get_expected_counts(res[2]))
```

Running the above code gives:

```shell

Chi Squared Test Statistic = 32.073
Critical value at P-value of 0.05 is 15.51

False
```

As expected, the above test fails because the test statistic exceeds the critical value from the chi-squared test.

Next, let's use a data set from [Impractical Python Projects GitHub repository](https://github.com/rlvaugh/Impractical_Python_Projects). Among other things, it contains data from the 2016 US presidential election: final by-county votes for 102 counties in Illinois. Let's apply our test on the votes for Hillary Clinton and Donald Trump.

```python
clinton_votes = ['7676','1262','2068','8986','476','6029','739','2447','1621',\
                 '50137','3992','1877','1020','3945','7309','1611946','1992',\
                 '1031','20466','1910','1949','228622','1793','434','3083',\
                 '1819','1414','4727','6133','657','1205','8065','802','2139',\
                 '420','1155','8871','2504','11634','924','4425','2679','4462',\
                 '1142','103665','18971','24884','10083','171095','19543',\
                 '1290','5528','4023','3313','18343','6689','50587','4369',\
                 '1789','2014','1558','5288','60803','36196','1817','3071',\
                 '5535','3504','4696','1481','8050','38060','2462','2645',\
                 '1413','375','962','1147','3439','1584','32298','2572',\
                 '40907','1075','535','2288','60756','751','7768','20685',\
                 '2402','10039','1151','2987','1448','1048','1412','11035',\
                 '151927','8581','55713','5092']

res = count_first_digits(clinton_votes)
chi_square_test(res[0], get_expected_counts(res[2]))

trump_votes = ['22790','1496','4888','12282','1796','9281','1721','4434',\
               '3216','33368','10543','5622','5021','12412','13003','453287',\
               '6277','4206','19091','5077','5698','166415','5645','2778',\
               '13635','7372','4480','13116','8492','1942','4145','13454',\
               '3206','6430','1653','2155','13985','9750','10843','3975',\
               '11695','7748','6121','4649','82734','25129','24961','10737',\
               '109767','26689','4521','8612','10208','8181','26866','14322',\
               '70490','11859','3785','4058','4846','6795','71612','37237',\
               '4231','4807','12629','8630','9076','4455','14352','35633',\
               '6855','5634','5754','1678','1675','1767','10023','5739',\
               '26998','8276','49944','2524','1966','8229','53857','1778',\
               '11083','38707','5790','19087','4047','4275','5571','6967',\
               '5640','12615','132720','21570','55624','13207']

res = count_first_digits(trump_votes)
chi_square_test(res[0], get_expected_counts(res[2]))
```

Running the above code gives us:

```shell

Chi Squared Test Statistic = 4.420
Critical value at P-value of 0.05 is 15.51

Chi Squared Test Statistic = 15.129
Critical value at P-value of 0.05 is 15.51

True
```


