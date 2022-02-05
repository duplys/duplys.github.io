---
layout: post
title:  "SSH-KEYGEN RSA"
date:   2022-01-29 14:05:30 +0100
categories: crypto programming
---

# Motivation
While looking at how RSA works, a colleague asked me how much time it takes to generate an RSA key pair (since you need to find two large primes p and q in the first place). I fired up a shell and ran `ssh-keygen` to demonstrate that it is reasonably fast. The colleague then asked how `ssh-keygen` manages to generate these keys, and specifically to find the primes p and q so fast. I couldn't answer that question and so started looking into the code. This is the description of my small journey.

# Where is the Code?
If you look into the `ssh-keygen` [manpage on Ubuntu](https://manpages.ubuntu.com/manpages/xenial/man1/ssh-keygen.1.html) for `xenial` release, it turns out that the `ssh-keygen` utility comes from OpenSSH. In the AUTHORS section of the manpage it says:

> OpenSSH is a derivative of the original and free ssh 1.2.12 release by Tatu Ylonen.  Aaron Campbell, Bob Beck, Markus Friedl, Niels Provos, Theo de Raadt and Dug Song removed many bugs, re-added newer features and created OpenSSH.  Markus Friedl contributed the support for SSH protocol versions 1.5 and 2.0.

The OpenSSH code is hosted in [openssh/openssh-portable](https://github.com/openssh/openssh-portable) Git repository on GitHub.

!["ddd"](/assets/openssh-readme.png "OpenSSH README.md")

In `ssh-keygen.c`, line 3792 in function `main`:

```c
...
if ((r = sshkey_generate(type, bits, &private)) != 0)
	fatal("sshkey_generate failed");
break;
...
```

The function `sshkey_generate` is defined in `sshkey.c`:

```bash
paulduplys@Pauls-MBP openssh-portable % grep "sshkey_generate" *
grep: contrib: Is a directory
grep: m4: Is a directory
grep: openbsd-compat: Is a directory
grep: regress: Is a directory
ssh-keygen.c:		if ((r = sshkey_generate(type, bits, &private)) != 0) {
ssh-keygen.c:			error_r(r, "sshkey_generate failed");
ssh-keygen.c:		if ((r = sshkey_generate(type, bits, &private)) != 0)
ssh-keygen.c:			fatal("sshkey_generate failed");
sshkey.c:sshkey_generate(int type, u_int bits, struct sshkey **keyp)
sshkey.h:int		 sshkey_generate(int type, u_int bits, struct sshkey **keyp);
paulduplys@Pauls-MBP openssh-portable % 
```

There the `sshkey_generate` function is defined as:

```c
int
sshkey_generate(int type, u_int bits, struct sshkey **keyp)
{
	struct sshkey *k;
	int ret = SSH_ERR_INTERNAL_ERROR;

	if (keyp == NULL)
		return SSH_ERR_INVALID_ARGUMENT;
	*keyp = NULL;
	if ((k = sshkey_new(KEY_UNSPEC)) == NULL)
		return SSH_ERR_ALLOC_FAIL;
	switch (type) {
	case KEY_ED25519:
		if ((k->ed25519_pk = malloc(ED25519_PK_SZ)) == NULL ||
		    (k->ed25519_sk = malloc(ED25519_SK_SZ)) == NULL) {
			ret = SSH_ERR_ALLOC_FAIL;
			break;
		}
		crypto_sign_ed25519_keypair(k->ed25519_pk, k->ed25519_sk);
		ret = 0;
		break;
#ifdef WITH_XMSS
	case KEY_XMSS:
		ret = sshkey_xmss_generate_private_key(k, bits);
		break;
#endif /* WITH_XMSS */
#ifdef WITH_OPENSSL
	case KEY_DSA:
		ret = dsa_generate_private_key(bits, &k->dsa);
		break;
# ifdef OPENSSL_HAS_ECC
	case KEY_ECDSA:
		ret = ecdsa_generate_private_key(bits, &k->ecdsa_nid,
		    &k->ecdsa);
		break;
# endif /* OPENSSL_HAS_ECC */
	case KEY_RSA:
		ret = rsa_generate_private_key(bits, &k->rsa);
		break;
#endif /* WITH_OPENSSL */
	default:
		ret = SSH_ERR_INVALID_ARGUMENT;
	}
	if (ret == 0) {
		k->type = type;
		*keyp = k;
	} else
		sshkey_free(k);
	return ret;
}
```

and this is what `rsa_generate_private_key` looks like (define in the same file):

```c
#ifdef WITH_OPENSSL
static int
rsa_generate_private_key(u_int bits, RSA **rsap)
{
	RSA *private = NULL;
	BIGNUM *f4 = NULL;
	int ret = SSH_ERR_INTERNAL_ERROR;

	if (rsap == NULL)
		return SSH_ERR_INVALID_ARGUMENT;
	if (bits < SSH_RSA_MINIMUM_MODULUS_SIZE ||
	    bits > SSHBUF_MAX_BIGNUM * 8)
		return SSH_ERR_KEY_LENGTH;
	*rsap = NULL;
	if ((private = RSA_new()) == NULL || (f4 = BN_new()) == NULL) {
		ret = SSH_ERR_ALLOC_FAIL;
		goto out;
	}
	if (!BN_set_word(f4, RSA_F4) ||
	    !RSA_generate_key_ex(private, bits, f4, NULL)) {
		ret = SSH_ERR_LIBCRYPTO_ERROR;
		goto out;
	}
	*rsap = private;
	private = NULL;
	ret = 0;
 out:
	RSA_free(private);
	BN_free(f4);
	return ret;
}

...

#endif /* WITH_OPENSSL */
```