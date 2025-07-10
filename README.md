# Description

DictDiffer is a comparison tool for Python dictionaries that supports three modes of comparison: text, JSON, and flat. It provides a structured way to identify differences between two dictionaries, making it useful for debugging and data validation.

# Example

```
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