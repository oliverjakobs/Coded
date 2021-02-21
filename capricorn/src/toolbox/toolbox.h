#ifndef TOOLBOX_H
#define TOOLBOX_H

#include <stdlib.h>
#include <stddef.h>
#include <string.h>

/*
 * Define TB_NOASSERT to compile out all assertions used internally.
 */
/* #define TB_NOASSERT */
#ifndef TB_NOASSERT
#include <assert.h>
#define TB_ASSERT(expr) assert(expr)
#else
#define TB_ASSERT(expr)
#endif

#include <stdint.h>

void tb_swap(void** a, void** b);
void tb_swap_i(int* a, int* b);
void tb_swap_i32(int32_t* a, int32_t* b);
void tb_swap_i64(int64_t* a, int64_t* b);
void tb_swap_f(float* a, float* b);
void tb_swap_str(char** a, char** b);

inline int tb_max_i(int a, int b) { return a > b ? a : b; }
inline int32_t tb_max_i32(int32_t a, int32_t b) { return a > b ? a : b; }
inline int64_t tb_max_i64(int64_t a, int64_t b) { return a > b ? a : b; }
inline float tb_max_f(float a, float b) { return a > b ? a : b; }

inline int tb_min_i(int a, int b) { return a < b ? a : b; }
inline int32_t tb_min_i32(int32_t a, int32_t b) { return a < b ? a : b; }
inline int64_t tb_min_i64(int64_t a, int64_t b) { return a < b ? a : b; }
inline float tb_min_f(float a, float b) { return a < b ? a : b; }

inline uint8_t tb_between_i(int start, int end, int value) { return (value <= end) && (value >= start); }
inline uint8_t tb_between_i32(int32_t start, int32_t end, int32_t value) { return (value <= end) && (value >= start); }
inline uint8_t tb_between_i64(int64_t start, int64_t end, int64_t value) { return (value <= end) && (value >= start); }
inline uint8_t tb_between_f(float start, float end, float value) { return (value <= end) && (value >= start); }


#endif /* !TOOLBOX_H */
