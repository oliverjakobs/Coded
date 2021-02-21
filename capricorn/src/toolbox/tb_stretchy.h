#ifndef TB_STRETCHY_H
#define TB_STRETCHY_H

#include <stdlib.h>

#define TB_STRETCHY_HDR_ELEM	size_t
#define TB_STRETCHY_HDR_SIZE	2 * sizeof(TB_STRETCHY_HDR_ELEM)

#define tb_stretchy__max(a, b) ((a) >= (b) ? (a) : (b))

#define tb_stretchy__hdr(b) ((size_t*)(void*)(b) - 2)
#define tb_stretchy__cap(b) tb_stretchy__hdr(b)[0]
#define tb_stretchy__len(b) tb_stretchy__hdr(b)[1]

#define tb_stretchy_len(b) ((b) ? tb_stretchy__len(b) : 0)
#define tb_stretchy_cap(b) ((b) ? tb_stretchy__cap(b) : 0)

#define tb_stretchy_resize(b, n)    (*((void**)&(b)) = tb_stretchy__resize((b), (n), sizeof(*(b))))
#define tb_stretchy_reserve(b, n)   (*((void**)&(b)) = tb_stretchy__reserve((b), (n), sizeof(*(b))))
#define tb_stretchy_grow(b, n)      (*((void**)&(b)) = tb_stretchy__grow((b), (n), sizeof(*(b))))
#define tb_stretchy_free(b)         ((b) ? (free(tb_stretchy__hdr(b)), (b) = NULL) : 0);

#define tb_stretchy_push(b, v) (tb_stretchy_grow((b), 1), (b)[tb_stretchy__len(b)++] = (v))

#define tb_stretchy_pack(b) (tb_stretchy_resize((b), tb_stretchy_len(b)))
#define tb_stretchy_clear(b) ((b) ? tb_stretchy__len(b) = 0 : 0)

#define tb_stretchy_last(b) ((b) + tb_stretchy_len(b))
#define tb_stretchy_sizeof(b) (tb_stretchy_len(b) * sizeof(*(b)))

static void* tb_stretchy__resize(void* buf, size_t new_cap, size_t elem_size)
{
    size_t hdr_size = 2 * sizeof(size_t);
    size_t* hdr = realloc(buf ? tb_stretchy__hdr(buf) : NULL, hdr_size + (new_cap * elem_size));

    if (!hdr) return NULL; /* out of memory */

    hdr[0] = new_cap;
    if (!buf) hdr[1] = 0;

    return hdr + 2;
}

static void* tb_stretchy__grow(void* buf, size_t increment, size_t elem_size)
{
    if (buf && tb_stretchy__len(buf) + increment < tb_stretchy__cap(buf))
        return buf;

    size_t new_size = tb_stretchy_len(buf) + increment;
    size_t new_cap = tb_stretchy__max((buf ? 2 * tb_stretchy__cap(buf) : 1), new_size);

    return tb_stretchy__resize(buf, new_cap, elem_size);
}

static void* tb_stretchy__reserve(void* buf, size_t reserve, size_t elem_size)
{
    if (buf && reserve < tb_stretchy__cap(buf))
        return buf;

    return tb_stretchy__resize(buf, reserve, elem_size);
}

#endif // !TB_STRETCHY_H
