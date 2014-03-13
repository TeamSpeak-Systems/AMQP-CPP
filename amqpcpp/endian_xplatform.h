#ifdef _WIN32
#include <stdlib.h>
inline uint16_t  htobe16(uint16_t value) { return _byteswap_ushort(value);}
inline uint32_t  htobe32(uint32_t value) { return _byteswap_ulong(value);}
inline uint64_t  htobe64(uint64_t value) { return _byteswap_uint64(value);}

inline uint16_t  be16toh(uint16_t value) { return _byteswap_ushort(value);}
inline uint32_t  be32toh(uint32_t value) { return _byteswap_ulong(value);}
inline uint64_t  be64toh(uint64_t value) { return _byteswap_uint64(value);}
#else
#include <endian.h>
#endif