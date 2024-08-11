#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "src/base64.h"

int main() {
	char *string = "test";
	size_t inlen = strlen(string);
	char *out = (char *) malloc(BASE64_ENCODE_OUT_SIZE(inlen));
	size_t result = base64_encode ( (unsigned const char *) string, inlen, out);
	char *de_str = (char *) malloc(BASE64_DECODE_OUT_SIZE(result));
	base64_decode((unsigned const char *) out, result, de_str);
	
	return 0;
}

