#ifndef LOGGER_H
#define LOGGER_H

#if _DEBUG

#define DEBUG_ENABLE_LOGGING

#endif

/*
 * -----------------------------------------------------------------------------------
 *                               Debug Logging
 * -----------------------------------------------------------------------------------
 */
#ifdef DEBUG_ENABLE_LOGGING

#include <stdio.h>
#include <stdarg.h>

#define DEBUG_TRACE(s, ...)		logger_write(stdout, LOG_TRACE, s, __VA_ARGS__)
#define DEBUG_INFO(s, ...)		logger_write(stdout, LOG_INFO, s, __VA_ARGS__)
#define DEBUG_WARN(s, ...)		logger_write(stdout, LOG_WARN, s, __VA_ARGS__)
#define DEBUG_ERROR(s, ...)		logger_write(stdout, LOG_ERROR, s, __VA_ARGS__)
#define DEBUG_CRITICAL(s, ...)	logger_write(stdout, LOG_CRITICAL, s, __VA_ARGS__)

#else

#define DEBUG_TRACE(s, ...)
#define DEBUG_INFO(s, ...)
#define DEBUG_WARN(s, ...)
#define DEBUG_ERROR(s, ...)
#define DEBUG_CRITICAL(s, ...)

#endif

typedef enum
{
    LOG_TRACE,
    LOG_INFO,
    LOG_WARN,
    LOG_ERROR,
    LOG_CRITICAL
} LogLevel;

void logger_write(FILE* const stream, LogLevel level, const char* fmt, ...);

#endif // !LOGGER_H
