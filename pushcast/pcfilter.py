'''
Created on Aug 24, 2015

@author: anotherpyr
'''
class SimpleDescription():
    def filter(self, lines):
        output = u""
        append = False
        
        for k in range(0, len(lines)):
            line = lines[k]
           
            # Remove excess URLs from descriptions 
            if line.find("://") < 0:
                if append:
                    output += u" "
                else:
                    append = True
                    
                output += line
            
        # if this removed all of the lines
        if len(output) < 1:
            #Then remove just URLs (could be humorous
            for k in range(0, len(lines)):
                if append:
                    output += u" "
                else:
                    append = True
                    
                output += lines[k]

        output = output.replace("<p>", "")
        output = output.replace("</p>", "")
        output = output.replace("<span>", "")
        output = output.replace("</span>", "")
        
        return output