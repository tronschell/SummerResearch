from company_name import *

def find_paragraphs(p_wordlist, s_wordlist, full_paragraphs, current_cik, documents, doc, section, unicount, found_dict):
    foundcount = 0
    if section.lower == "item 7":
        for p_word in range(len(p_wordlist)):
                    # For every line in the range of the length of the "full_paragraphs" run the codfe underneath
                    for j in range(len(full_paragraphs)):

                        # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                        if p_wordlist[p_word] in full_paragraphs[j].get_text():
                            try:
                                found = str(full_paragraphs[j].get_text())

                                # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                                before_found = str(full_paragraphs[j-1].get_text())
                                while len(before_found) <= 2:
                                    foundcount +=1
                                    before_found = str(full_paragraphs[j-foundcount].get_text())

                                # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
                                after_found = str(full_paragraphs[j+1].get_text())

                                # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                                while len(after_found) <= 2:
                                    foundcount +=1
                                    after_found = str(full_paragraphs[j+foundcount].get_text())
                                unicount +=1
                                #For every secondary word in the secondary word list, run the code below
                                for s_word in range(len(s_wordlist)):
                                    paragraphthere = False
                                    # If there is a secondary word in the before paragraph, then run the code underneath
                                    if s_wordlist[s_word] in before_found:
                                        print("CIK: ", current_cik[doc])
                                        print('PRIMARY WORD: ', p_wordlist[p_word])
                                        print('SECONDARY WORD:', s_wordlist[s_word])
                                        print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++', '\n\n')
                                        if s_wordlist[s_word] in after_found:
                                            paragraphthere = True
                                        else:
                                            paragraphthere = False
                                            pass

                                        unicount+=1
                                        
                                        if paragraphthere == True:
                                            print("\tbefore: ",before_found, '\n\n')
                                            print("\tmatch: ",found, '\n\n')
                                            print("\tafter: ", after_found, '\n\n')
                                            print("----------------------")

                                            found_dict[unicount] = {
                                                "CIK" : current_cik[doc],
                                                "Company Name" : getCompanyName(documents[doc]),
                                                "Item": "7: Management’s Discussion and Analysis of Financial Condition and Results of Operations",
                                                "Primary Word" : p_wordlist[p_word],
                                                "Secondary Word" : s_wordlist[s_word],
                                                "before": before_found,
                                                "match" : found,
                                                "after" : after_found
                                            }
                                        else:
                                            print("\tbefore: ",before_found, '\n\n')
                                            print("\tmatch: ",found, '\n\n')
                                            print("----------------------")

                                            found_dict[unicount] = {
                                                "CIK" : current_cik[doc],
                                                "Company Name" : getCompanyName(documents[doc]),
                                                "Item": "7: Management’s Discussion and Analysis of Financial Condition and Results of Operations",
                                                "Primary Word" : p_wordlist[p_word],
                                                "Secondary Word" : s_wordlist[s_word],
                                                "before": before_found,
                                                "match" : found,
                                            }

                                    # Else if there is a secondary word in the after found paragraph, then run the code underneath
                                    elif s_wordlist[s_word] in after_found:
                                        print("CIK: ", current_cik[doc])
                                        print('PRIMARY WORD: ', p_wordlist[p_word])
                                        print('SECONDARY WORD:', s_wordlist[s_word])
                                        print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++', '\n\n')
                                        print("\tmatch: ",found, '\n\n')
                                        print("\tafter: ",after_found, '\n\n')
                                        print("----------------------")
                                        unicount+=1

                                        found_dict[unicount] = {
                                                "CIK" : current_cik[doc],
                                                "Company Name" : getCompanyName(documents[doc]),
                                                "Item": "7: Management’s Discussion and Analysis of Financial Condition and Results of Operations",
                                                "Primary Word" : p_wordlist[p_word],
                                                "Secondary Word" : s_wordlist[s_word],
                                                "match" : found,
                                                "after" : after_found
                                            }
                                    else:
                                        pass      
                            except:
                                pass
                            return current_cik[doc], found, after_found

    elif section.lower == "item 1a":
        for p_word in range(len(p_wordlist)):

                # For every line in the range of the length of the "full_paragraphs" run the codfe underneath
                for j in range(len(full_paragraphs)):

                    # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                    if p_wordlist[p_word] in full_paragraphs[j].get_text():
                        try:
                            found = str(full_paragraphs[j].get_text())

                            # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                            before_found = str(full_paragraphs[j-1].get_text())
                            while len(before_found) <= 2:
                                foundcount +=1
                                before_found = str(full_paragraphs[j-foundcount].get_text())

                            # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
                            after_found = str(full_paragraphs[j+1].get_text())

                            # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                            while len(after_found) <= 2:
                                foundcount +=1
                                after_found = str(full_paragraphs[j+foundcount].get_text())
                            unicount +=1
                            #For every secondary word in the secondary word list, run the code below
                            for s_word in range(len(s_wordlist)):
                                paragraphthere = False
                                # If there is a secondary word in the before paragraph, then run the code underneath
                                if s_wordlist[s_word] in before_found:
                                    print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', p_wordlist[p_word])
                                    print('SECONDARY WORD:', s_wordlist[s_word])
                                    print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                    # If there is a secondary word in the after found paragraph, then run the code underneath
                                    if s_wordlist[s_word] in after_found:
                                        paragraphthere = True
                                    else:
                                        paragraphthere = False
                                        pass
                                    
                                    unicount+=1

                                    if paragraphthere == True:
                                        print("\tbefore: ",before_found, '\n\n')
                                        print("\tmatch: ",found, '\n\n')
                                        print("\tafter: ", after_found, '\n\n')
                                        print("----------------------")

                                        found_dict[unicount] = {
                                            "CIK" : current_cik[doc],
                                            "Company Name" : getCompanyName(documents[doc]),
                                            "Item": "1A: Risk Factors",
                                            "Primary Word" : p_wordlist[p_word],
                                            "Secondary Word" : s_wordlist[s_word],
                                            "before": before_found,
                                            "match" : found,
                                            "after" : after_found
                                        }
                                    else:
                                        print("\tbefore: ",before_found, '\n\n')
                                        print("\tmatch: ",found, '\n\n')
                                        print("----------------------")

                                        found_dict[unicount] = {
                                            "CIK" : current_cik[doc],
                                            "Company Name" : getCompanyName(documents[doc]),
                                            "Item": "1A: Risk Factors",
                                            "Primary Word" : p_wordlist[p_word],
                                            "Secondary Word" : s_wordlist[s_word],
                                            "before": before_found,
                                            "match" : found,
                                        }
                                        

                                # Else if there is a secondary word in the after found paragraph, then run the code underneath
                                elif s_wordlist[s_word] in after_found:
                                    print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', p_wordlist[p_word])
                                    print('SECONDARY WORD:', s_wordlist[s_word])
                                    print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                    print("\tmatch: ",found, '\n\n')
                                    print("\tafter: ",after_found, '\n\n')
                                    print("----------------------")
                                    unicount +=1
                                    
                                    found_dict[unicount] = {
                                            "CIK" : current_cik[doc],
                                            "Company Name" : getCompanyName(documents[doc]),
                                            "Item": "1A: Risk Factors",
                                            "Primary Word" : p_wordlist[p_word],
                                            "Secondary Word" : s_wordlist[s_word],
                                            "match" : found,
                                            "after" : after_found
                                        }
                                else:
                                    pass
                        except:
                            pass
                        return found_dict[unicount]