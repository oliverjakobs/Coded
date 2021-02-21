#include "arena.h"

#include <string.h>
#include <assert.h>

#include "toolbox/tb_stretchy.h"

#define ALIGN_DOWN(n, a)        ((n) & ~((a) - 1))
#define ALIGN_UP(n, a)          ALIGN_DOWN((n) + (a) - 1, (a))
#define ALIGN_DOWN_PTR(p, a)    ((void *)ALIGN_DOWN((uintptr_t)(p), (a)))
#define ALIGN_UP_PTR(p, a)      ((void *)ALIGN_UP((uintptr_t)(p), (a)))

void arena_grow(Arena* arena, size_t min_size)
{
    size_t size = ALIGN_UP((ARENA_BLOCK_SIZE > min_size) ? ARENA_BLOCK_SIZE : min_size, ARENA_ALIGNMENT);
    arena->ptr = malloc(size);
    if (!arena->ptr)
    {
        perror("Failed to grow arena");
        exit(1);
    }

    arena->end = arena->ptr + size;
    tb_stretchy_push(arena->blocks, arena->ptr);
}

void* arena_alloc(Arena* arena, size_t size)
{
    if (size > (size_t)(arena->end - arena->ptr))
    {
        arena_grow(arena, size);
        assert(size <= (size_t)(arena->end - arena->ptr));
    }

    void* ptr = arena->ptr;
    arena->ptr = ALIGN_UP_PTR(arena->ptr + size, ARENA_ALIGNMENT);
    assert(arena->ptr <= arena->end);
    assert(ptr == ALIGN_DOWN_PTR(ptr, ARENA_ALIGNMENT));
    return ptr;
}

void* arena_dup(Arena* arena, void* src, size_t size)
{
    void* dest = arena_alloc(arena, size);
    memcpy(dest, src, size);
    return dest;
}

void arena_free(Arena* arena)
{
    for (char** it = arena->blocks; it != tb_stretchy_last(arena->blocks); it++)
        free(*it);
}