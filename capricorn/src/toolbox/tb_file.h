#ifndef TB_FILE_H
#define TB_FILE_H

#include <stdio.h>

char* tb_file_read(const char* path, const char* mode, size_t* sizeptr);

#endif /* !TB_FILE_H */