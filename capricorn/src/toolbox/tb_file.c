#include "tb_file.h"

#include <stdlib.h>

char* tb_file_read(const char* path, const char* mode, size_t* sizeptr)
{
	FILE* file = fopen(path, mode);
	if (!file) return NULL;

	/* find file size */
	fseek(file, 0, SEEK_END);
	size_t size = ftell(file);
	rewind(file);

	char* buffer = malloc(size + 1);
	if (!buffer)
	{
		fclose(file);
		return NULL;
	}

	if (fread(buffer, size, 1, file) != 1)
	{
		free(buffer);
		fclose(file);
		return NULL;
	}

	buffer[size] = '\0'; /* zero terminate buffer */
	if (sizeptr) *sizeptr = size + 1;

	fclose(file);
	return buffer;
}
