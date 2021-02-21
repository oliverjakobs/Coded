#ifndef MEMORY_ARENA
#define MEMORY_ARENA

#include <stdlib.h>

typedef struct
{
    char* ptr;
    char* end;
    char** blocks;
} Arena;

#define ARENA_ALIGNMENT 8
#define ARENA_BLOCK_SIZE (1024 * 1024)

void arena_grow(Arena* arena, size_t min_size);
void* arena_alloc(Arena* arena, size_t size);
void* arena_dup(Arena* arena, void* src, size_t size);

void arena_free(Arena* arena);

#endif // !MEMORY_ARENA
