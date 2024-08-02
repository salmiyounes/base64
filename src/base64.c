#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "base64.h"


size_t base64_encode (const unsigned char *in, size_t inlen, char *out) {
		size_t i, l;
		for (i = l = 0; i < inlen; i += 3) {
			out[l++] = 	base64en[(in[i] >> 2) & 0x3F];
			if (i < inlen -  1) {
				out[l++] = 		base64en[((in[i] & 0x03) << 4) | ((in[i+1] & 0xF0) >> 4)];
				if (i < inlen - 2) {
					out[l++] = 	base64en[((in[i + 1] & 0x0F) << 2) | ((in[i + 2] & 0xC0) >> 6)];
					out[l++] = 	base64en[in[i + 2] & 0x3F];
				} else {
					out[l++] = 	base64en[((in[i + 1] & 0x0F) << 2)];
					out[l++] = 	BASE64_PAD;
				}
			} else {
				out[l++] = 	base64en[((in[i] & 0x03) << 4) | 0];
				out[l++] =	BASE64_PAD;
				out[l++] =	BASE64_PAD;
			}
		}
		
		out[l] = 0;
		return l;
}

size_t base64_decode(const unsigned char *in, size_t inlen, char *out) {
	size_t i, l;
	unsigned char c1, c2, c3;
	
	for (i = l = 0; i < inlen; i += 4) {
		unsigned char b1 = (unsigned char)base64de[in[i]];
		unsigned char b2 = (unsigned char)base64de[in[i + 1]];
		unsigned char b3 = (unsigned char)base64de[in[i + 2]];
		unsigned char b4 = (unsigned char)base64de[in[i + 3]];
		
		if (in[i + 3] == BASE64_PAD) {
			if (in[i + 2] == BASE64_PAD) {
				c1 = (unsigned char)(b1 << 2 | ((b2 & 0xF0) >> 4));
				out[l++] = c1;
			} else {
				c1 = (unsigned char)(b1 << 2 | ((b2 & 0xF0) >> 4));
				c2 = (unsigned char)(((b2 & 0x0F) << 4) | ((b3 & 0x3C) >> 2));
				out[l++] = c1;
				out[l++] = c2;
			}
		} else {
			c1 = (unsigned char)(b1 << 2 | ((b2 & 0xF0) >> 4));
        		c2 = (unsigned char)(((b2 & 0x0F) << 4) | ((b3 & 0x3C) >> 2));
        		c3 = (unsigned char)(((b3 & 0x03) << 6) | (b4 & 0x3F));
			out[l++] = c1;
			out[l++] = c2;
			out[l++] = c3;
		}
	}
	
	return l;
}





















