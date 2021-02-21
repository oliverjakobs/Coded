#include "tb_str.h"

#include <stdlib.h>

char tb_tolower(unsigned char c)
{
    return (c >= 'A' && c <= 'Z') ? 'a' + (c - 'A') : c;
}

int tb_strcasecmp(const char* str1, const char* str2)
{
    const unsigned char* us1 = (const unsigned char*)str1;
    const unsigned char* us2 = (const unsigned char*)str2;

    while (tb_tolower(*us1) == tb_tolower(*us2++))
        if (*us1++ == '\0') return 0;

    return (tb_tolower(*us1) - tb_tolower(*--us2));
}

int tb_strncasecmp(const char* str1, const char* str2, size_t max_count)
{
	if (max_count != 0)
	{
		const unsigned char* us1 = (const unsigned char*)str1;
		const unsigned char* us2 = (const unsigned char*)str2;

		do
		{
			if (tb_tolower(*us1) != tb_tolower(*us2++))
				return tb_tolower(*us1) - tb_tolower(*--us2);

			if (*us1++ == '\0') break;
		} while (--max_count != 0);
	}
	return 0;
}

char* tb_strdup(const char* src)
{
    size_t len = strlen(src) + 1;
    char* dst = malloc(len);

    return dst ? memcpy(dst, src, len) : NULL;
}
