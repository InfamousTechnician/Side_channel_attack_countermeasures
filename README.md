# Side channel attack countermeasures

## A masked "AND" version I found out:

* masked_AND_by_me.py contains paramaterizable code to calculate "AND" between arbitrary many masked shares of two words of arbitrary bit widths. I discovered this function while studiing side channel attacks. It has NOT been proven SCA proof!! The function calculates Ci-s by "AND"-ing the corresponding bits Ai and Bi, and correcting this with the parities of all the other bits Aj and Bj, where j<>i by "AND"-ing the parities and XOR-ing this to the Ai&Bi product. Its advantage may be that it shouldn't need new random input data, and still the computations and the output could be safely masked. However the versions with offsets may generate more algorithmic noise if the offstes are randomized:

* and_offset.py may already be SCA proof, in fact it hopefully is a threshold implementation, with more or less randomly shufflable computations - these make analysis more noisy, if the attacker doesn't know which piece of trace belongs to which share, and thus has to sum up some trace pieces, like if they were implemented in parallel hardware and calculate with those algorithmically noisy results.

* and_offset_rolling.py implements a the previous offseted version a little bit simplified based on the fact that parity is like a "rolling hash", which can be updated element wise, and doesn't need the full recomputation for each AND-ed bit's corrections.

* rolled_out_masked_and.py describes if the parities weren't fully calculated, because they actually create the mask of the very last non-used share... insted, after re-reading the accompanying pdf, Glitch Resistant Masking Schemes, I got suspicious, that any odd number of shares can be used as a threshold implementation similar to the equation is the pdf, if I rolled out the compact, parity based equaton, what I described. And in this unrolled case the circuit never even ever gets close to disclosing one or another mask of any share.

## A masked AES S-box

* should protect against first order attacks
* is implemented with plain memory, requiring 64k entries thus (an original address byte and a randomized address byte yield 16 bits of address space)

## A boolean masked Montgomery exponentiation ladder

* its based on the accompanying scientific publication (pdf)...
* ...which states this algorithm should protect against first order side channel attacks, if registers don't leak
