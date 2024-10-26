# Phrase-Lock

A simple program allowing decryption and encryption of files using phrases.

## What it is

The program allows the user to add a layer of encryption to sensitive data. It takes a phrase of their choosing, which can be of any length, and uses it to generate a unique 256-bit key with which to either encrypt or decrypt a selected file or directory. This is intended for use where a user is unwilling to have access credentials stored anywhere besides their own memory.

The benefits include:
* Effectively password-protecting data without any limitations on length
* Avoiding any any reliance on third parties
* Avoiding having to save or write down a full-length secret key

## What it isn't

The program is **not** a substitute for using a randomly generated secret key. As any memorable phrase will generally be in natural language, they will be more vulnerable to brute-force attacks.