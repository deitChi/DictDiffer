import json

class DictDiffer:
    def __init__(self, dict1, dict2, mode='text'):
        self.dict1 = dict1
        self.dict2 = dict2
        self.mode = mode
        self.flat_changes = []

    def compare(self):
        if self.mode == 'text':
            return self._compare_text(self.dict1, self.dict2)
        elif self.mode == 'json':
            return self._compare(self.dict1, self.dict2)
        elif self.mode == 'flat':
            self._compare(self.dict1, self.dict2, path=[])
            return self.flat_changes
            

    # === TEXT OUTPUT ===
    def _compare_text(self, a, b, indent=1):
        if isinstance(a, dict) and isinstance(b, dict):
            return self._compare_text_dicts(a, b, indent)
        elif isinstance(a, list) and isinstance(b, list):
            return self._compare_text_lists(a, b, indent)
        elif isinstance(a, tuple) and isinstance(b, tuple):
            return self._compare_text_lists(list(a), list(b), indent, wrap="()")
        elif isinstance(a, set) and isinstance(b, set):
            return self._compare_text_sets(a, b, indent)
        elif a == b:
            return f"{json.dumps(a)}\n"
        else:
            a_str = "null" if a is None else json.dumps(a)
            b_str = "null" if b is None else json.dumps(b)
            return f"{a_str} -> {b_str}\n"

    def _compare_text_dicts(self, d1, d2, indent):
        indent_str = "\t" * indent
        keys = list(d1.keys()) + [k for k in d2 if k not in d1]
        result = "{\n"
        for key in keys:
            val1 = d1.get(key)
            val2 = d2.get(key)
            result += f"{indent_str}\"{key}\": "
            result += self._compare_text(val1, val2, indent + 1)
        result += "\t" * (indent - 1) + "}\n"
        return result

    def _compare_text_lists(self, l1, l2, indent, wrap="[]"):
        max_len = max(len(l1), len(l2))
        indent_str = "\t" * indent
        result = f"{wrap[0]}\n"
        for i in range(max_len):
            val1 = l1[i] if i < len(l1) else None
            val2 = l2[i] if i < len(l2) else None
            result += indent_str
            if isinstance(val1, dict) and isinstance(val2, dict):
                result += self._compare_text_dicts(val1, val2, indent + 1).rstrip() + "\n"
            elif val1 == val2:
                result += json.dumps(val1) + "\n"
            elif val1 is not None and val2 is None:
                result += json.dumps(val1) + " -> null\n"
            elif val1 is None and val2 is not None:
                result += "null -> " + json.dumps(val2) + "\n"
            else:
                result += json.dumps(val1) + " -> " + json.dumps(val2) + "\n"
        result += "\t" * (indent - 1) + wrap[1] + "\n"
        return result

    def _compare_text_sets(self, s1, s2, indent):
        indent_str = "\t" * indent
        removed = sorted(s1 - s2)
        added = sorted(s2 - s1)
        result = "{\n"
        if removed:
            result += indent_str + f"removed: {json.dumps(removed)}\n"
        if added:
            result += indent_str + f"added: {json.dumps(added)}\n"
        if not removed and not added:
            result += indent_str + "{}\n"
        result += "\t" * (indent - 1) + "}\n"
        return result

    # === JSON STRUCTURED DIFF ===
    def _compare(self, a, b, path=None):
        if path is None:
            path = []

        if isinstance(a, dict) and isinstance(b, dict):
            return self._compare_dicts(a, b, path)
        elif isinstance(a, list) and isinstance(b, list):
            return self._compare_lists(a, b, path)
        elif isinstance(a, tuple) and isinstance(b, tuple):
            return self._compare_lists(list(a), list(b), path)
        elif isinstance(a, set) and isinstance(b, set):
            return self._compare_sets(a, b)
        elif a == b:
            return {"unchanged": a}
        else:
            if self.mode == 'flat':
                self.flat_changes.append({"path": path, "from": a, "to": b})
            return {"from": a, "to": b}

    def _compare_dicts(self, d1, d2, path):
        keys = list(d1.keys()) + [k for k in d2 if k not in d1]
        result = {}
        for key in keys:
            val1 = d1.get(key)
            val2 = d2.get(key)
            new_path = path + [key]
            if key in d1 and key in d2:
                result[key] = self._compare(val1, val2, new_path)
            elif key in d1:
                if self.mode == 'flat':
                    self.flat_changes.append({"path": new_path, "from": val1, "to": None})
                result[key] = {"from": val1, "to": None}
            elif key in d2:
                if self.mode == 'flat':
                    self.flat_changes.append({"path": new_path, "from": None, "to": val2})
                result[key] = {"from": None, "to": val2}
        return result

    def _compare_lists(self, l1, l2, path):
        max_len = max(len(l1), len(l2))
        result = {}
        for i in range(max_len):
            val1 = l1[i] if i < len(l1) else None
            val2 = l2[i] if i < len(l2) else None
            new_path = path + [i]
            if isinstance(val1, dict) and isinstance(val2, dict):
                result[str(i)] = {"changes": self._compare_dicts(val1, val2, new_path)}
            else:
                result[str(i)] = self._compare(val1, val2, new_path)
        return result

    def _compare_sets(self, s1, s2):
        removed = sorted(s1 - s2)
        added = sorted(s2 - s1)
        result = {}
        if removed:
            result["removed"] = removed
        if added:
            result["added"] = added
        if not result:
            result["unchanged"] = sorted(s1)
        return result