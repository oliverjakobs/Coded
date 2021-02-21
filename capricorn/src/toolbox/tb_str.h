#ifndef TB_STRING_H
#define TB_STRING_H

#include <string.h>

char tb_tolower(unsigned char c);

int tb_strcasecmp(const char* str1, const char* str2);
int tb_strncasecmp(const char* str1, const char* str2, size_t max_count);

char* tb_strdup(const char* src);

#endif /* !TB_STRING_H */
