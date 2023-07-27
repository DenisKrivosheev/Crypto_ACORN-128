# Crypto_ACORN-128
This is my realization of Acorn-128 Chipher as course work (not verified as true calculated, somewhich functions of original will not realized)

# ALL CALCULATES IS ONLY +- EXAMPLES OF ANSWERS

Step 1: Key Expansion
Choose a secret key: "ABCDEFGHIJKLMNOP"<br />
Split the key into four 32-bit words: K0 = "ABCD", K1 = "EFGH", K2 = "IJKL", K3 = "MNOP" <br />

Step 2: Nonce
Choose a nonce: "12345678"
Split the nonce into four 32-bit words: N0 = "1234", N1 = "5678", N2 = "0000", N3 = "0000" <br />

Step 3: Initialization
Plaintext: "HELLO"
Split into two 32-bit blocks: L = "HE", R = "LLO"

Step 4: Encryption Rounds
Perform 20 encryption rounds. For each round:

Round 1:
Generate round key RK: Let's assume RK = "1234"
Calculate K4 = (ROL("ABCD", 1) + ROL("IJKL", 1)) XOR (ROR("MNOP", 1) + ROR("1234", 1)) = "RSTU"<br />
Calculate K5 = (ROL("EFGH", 1) + ROL("MNOP", 1)) XOR (ROR("IJKL", 1) + ROR("1234", 1)) = "VWXY"<br />
Calculate T1 = (L + R + "RSTU") mod 2^32 = "ZABC"<br />
Calculate T2 = (L + (2 * R) + "VWXY") mod 2^32 = "DEFG"<br />
Update L = "ZABC", R = "DEFG"<br />

Round 2:
Generate round key RK: Let's assume RK = "5678"<br />
Calculate K4 = (ROL("RSTU", 1) + ROL("DEFG", 1)) XOR (ROR("ABCD", 1) + ROR("5678", 1)) = "HIJK"<br />
Calculate K5 = (ROL("VWXY", 1) + ROL("ABCD", 1)) XOR (ROR("DEFG", 1) + ROR("5678", 1)) = "LMNO"<br />
Calculate T1 = (L + R + "HIJK") mod 2^32 = "PQRS"<br />
Calculate T2 = (L + (2 * R) + "LMNO") mod 2^32 = "TUVW"<br />
Update L = "PQRS", R = "TUVW"<br />

Continue the remaining 18 rounds, following the same steps.

Step 5: Finalization
After completing 20 encryption rounds, we obtain the final ciphertext.

For example, after 20 rounds, the final ciphertext could be: CT = "KQSMXVAF"
Step 4: Finalization

Swap the values of L and R: L = "TUVW", R = "PQRS"
Step 5: Ciphertext

Concatenate the final values of L and R: Ciphertext = "TUVW" + "PQRS" = "TUVWPQRS"
_________________________________________________________________________________________________________________________________________________________________________
# DECIPHERING
Use same algorithm but with chiphertext
