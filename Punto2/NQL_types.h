#ifndef NQL_TYPES_H
#define NQL_TYPES_H

#define MAX_TABLES 10
#define MAX_RECORDS 100
#define MAX_FIELDS 20
#define MAX_FIELD_NAME 50
#define MAX_VALUE_LEN 256

typedef enum { TYPE_NUMBER, TYPE_STRING, TYPE_BOOL, TYPE_NULL } ValueType;

typedef struct {
    ValueType type;
    union {
        double num;
        char str[MAX_VALUE_LEN];
        int boolean;
    } data;
} Value;

typedef struct {
    char name[MAX_FIELD_NAME];
    Value value;
} Field;

typedef struct {
    int id;
    Field fields[MAX_FIELDS];
    int field_count;
    int active;
} Record;

typedef struct {
    char name[MAX_FIELD_NAME];
    Record records[MAX_RECORDS];
    int record_count;
    int next_id;
} Table;

#endif

