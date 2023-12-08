class Commons():

    @staticmethod
    def check_for_space(path:str):
        characters = list(path)
        for i in range(0, len(characters)):
            # set the char[i] to this if char == to '\', '(', ')' otherwise, just leave as it is
            characters[i] = '\\ 'if (characters[i] == ' ') and characters[i-1] != '\\' else characters[i]
            characters[i] = '\(' if characters[i] == '(' else characters[i]
            characters[i] = '\)' if characters[i] == ')' else characters[i]

        def convert_list_to_string(li):
            temp = ""
            for i in li:
                temp += i
            return temp

        return convert_list_to_string(characters)