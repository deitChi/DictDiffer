# Description

DictDiffer is a comparison tool for Python dictionaries that supports three modes of comparison: text, JSON, and flat. It provides a structured way to identify differences between two dictionaries, making it useful for debugging and data validation.

# Example

```
# Text mode comparison

{
        "host_name": "abc_123" -> "abc_126"
        "address": "123.123.123.0"
        "attributes": {
                "max_check_attempts": 5 -> 6
                "time_period": "24x7" -> null
                "max_load_attempts": null -> 7
        }
        "list_of_data": [
                {
                        "name": "harry" -> "barry"
                        "age": null -> 22
                }
                {
                        "name": "barry" -> "garry"
                        "age": 21 -> 19
                        "type": null -> "employee"
                }
        ]
        "meta": {
                "coordinates": (
                        10
                        20 -> 30
                )
                "tags": {
                        removed: ["x"]
                        added: ["a"]
                }
        }
}
```

```
# JSON readable

{
  "host_name": {
    "from": "abc_123",
    "to": "abc_126"
  },
  "address": {
    "unchanged": "123.123.123.0"
  },
  "attributes": {
    "max_check_attempts": {
      "from": 5,
      "to": 6
    },
    "time_period": {
      "from": "24x7",
      "to": null
    },
    "max_load_attempts": {
      "from": null,
      "to": 7
    }
  },
  "list_of_data": {
    "0": {
      "changes": {
        "name": {
          "from": "harry",
          "to": "barry"
        },
        "age": {
          "from": null,
          "to": 22
        }
      }
    },
    "1": {
      "changes": {
        "name": {
          "from": "barry",
          "to": "garry"
        },
        "age": {
          "from": 21,
          "to": 19
        },
        "type": {
          "from": null,
          "to": "employee"
        }
      }
    }
  },
  "meta": {
    "coordinates": {
      "0": {
        "unchanged": 10
      },
      "1": {
        "from": 20,
        "to": 30
      }
    },
    "tags": {
      "removed": [
        "x"
      ],
      "added": [
        "a"
      ]
    }
  }
}
```

```
# FLAT OUTPUT

host_name : abc_123 -> abc_126
attributes -> max_check_attempts : 5 -> 6
attributes -> time_period : 24x7 -> None
attributes -> max_load_attempts : None -> 7
list_of_data -> 0 -> name : harry -> barry
list_of_data -> 0 -> age : None -> 22
list_of_data -> 1 -> name : barry -> garry
list_of_data -> 1 -> age : 21 -> 19
list_of_data -> 1 -> type : None -> employee
meta -> coordinates -> 1 : 20 -> 30
```