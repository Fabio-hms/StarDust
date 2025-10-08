from afn_to_afd import AFN, afn_to_afd

class Lexer:
    def __init__(self, afd, token_map):
        self.afd = afd
        self.token_map = token_map

    def tokenize(self, text):
        tokens = []
        i = 0
        while i < len(text):
            state = self.afd['start']
            j = i
            last_final = None
            last_final_pos = i
            while j < len(text):
                symbol = text[j]
                key = (state, symbol)
                if key in self.afd['transitions']:
                    state = self.afd['transitions'][key]
                    if state in self.afd['finals']:
                        last_final = state
                        last_final_pos = j + 1
                    j += 1
                else:
                    break
            if last_final:
                token_type = self.token_map.get(last_final, "UNKNOWN")
                token_value = text[i:last_final_pos]
                tokens.append((token_type, token_value))
                i = last_final_pos
            else:
                i += 1
        return tokens
