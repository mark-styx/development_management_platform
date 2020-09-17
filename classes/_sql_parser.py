class sql_parser():
    
    def __init__(self,fpath):
        self.comm_idx,self.comments,self.no_comm = self.comm_hndlr(fpath)
        self.tbl_ref = self.table_ref_indexer(self.no_comm)
        self.temp_created = self.temp_tables_created(self.no_comm)
        self.var_init = self.vars_created(self.no_comm)
        self.var_ref = self.vars_referenced(self.no_comm)

    def comm_hndlr(self,fpath):
        with open(fpath,'r') as f:
            lines = f.readlines()
        comm_idx = self.comment_indexer(lines)
        comments = self.comment_retreiver(lines,comm_idx)
        no_comm_lines = self.del_comments(lines,comm_idx)
        return (comm_idx,comments,no_comm_lines)

    def comment_indexer(self,lines):
        comm_idx = {'sl':[],'mls':[],'mle':[]}
        for idx,line in enumerate(lines):
            if '--' in line: comm_idx['sl'].append(idx)
            if '/*' in line: comm_idx['mls'].append(idx)
            if '*/' in line: comm_idx['mle'].append(idx)
        return comm_idx
        
    def del_comments(self,lines,comm_idx):
        for idx in comm_idx['sl']:
            lines[idx] = lines[idx][:lines[idx].find('--')].strip()
        for ist,ien in zip(comm_idx['mls'],comm_idx['mle']):
            for line in range(ist,ien):
                if line == ist: lines[line] = lines[line][:lines[line].find('/*')]
                elif line == ien: lines[line] = lines[line][lines[line].find('*/'):]
                else: lines.remove(lines[line])
        lines = [x for x in lines if x.strip()]
        return lines

    def comment_retreiver(self,lines,comm_idx):
        comments = {}
        for idx in comm_idx['sl']:
            comments[idx] = lines[idx][lines[idx].find('--'):].strip()
        for ist,ien in zip(comm_idx['mls'],comm_idx['mle']):
            comm = ' '.join(lines[ist:ien])
            comments[ist] = comm[comm.find('/*'):comm.find('*/')].strip()
        return comments

    def find(self,obj_flags,line): return [x for x in obj_flags if x in line]
    def find_ref(self,obj_flags,line):
        flags = []
        for x in obj_flags:
            for v in line:
                if x in v: flags.append(v)
        return flags

    def table_ref_indexer(self,no_comm_lines):
        obj_flags = ['from','update','join','delete','table','into']
        no_comm_lines = [x.split() for x in no_comm_lines]
        ref_ind = []
        for idx,line in enumerate(no_comm_lines):   
            flags = self.find(obj_flags,line)
            while flags:
                for flag in flags:
                    ref_ind.append((idx,line[line.index(flag) + 1]))
                    line.remove(flag)
                flags = self.find(obj_flags,line)
        ref_ind = [(x[0],x[1].replace('(','').replace(')','')) for x in ref_ind if x[1].replace('(','').replace(')','')]
        ref_ind = [(x[0],x[1]) for x in ref_ind if '.' in x[1] or '#' in x[1]]
        return ref_ind

    def temp_tables_created(self,no_comm_lines):
        obj_flags = ['into','create table']
        no_comm_lines = [x.split() for x in no_comm_lines]
        ref_ind = []
        for idx,line in enumerate(no_comm_lines):   
            flags = self.find(obj_flags,line)
            while flags:
                for flag in flags:
                    ref_ind.append((idx,line[line.index(flag) + 1]))
                    line.remove(flag)
                flags = self.find(obj_flags,line)
        ref_ind = [(x[0],x[1].replace('(','').replace(')','')) for x in ref_ind if x[1].replace('(','').replace(')','')]
        ref_ind = [(x[0],x[1]) for x in ref_ind if '#' in x[1]]
        return ref_ind

    def vars_referenced(self,no_comm_lines):
        obj_flags = ['@']
        no_comm_lines = [x.split() for x in no_comm_lines]
        ref_ind = []
        for idx,line in enumerate(no_comm_lines):   
            flags = self.find_ref(obj_flags,line)
            while flags:
                for flag in flags:
                    ref_ind.append((idx,line[line.index(flag)]))
                    line.remove(flag)
                flags = self.find(obj_flags,line)
        ref_ind = [(x[0],x[1].replace('(','').replace(')','')) for x in ref_ind if x[1].replace('(','').replace(')','')]
        ref_ind = [(x[0],x[1]) for x in ref_ind if '@' in x[1]]
        return ref_ind

    def vars_created(self,no_comm_lines):
        obj_flags = ['declare']
        no_comm_lines = [x.split() for x in no_comm_lines]
        ref_ind = []
        for idx,line in enumerate(no_comm_lines):   
            flags = self.find(obj_flags,line)
            while flags:
                for flag in flags:
                    ref_ind.append((idx,line[line.index(flag) + 1]))
                    line.remove(flag)
                flags = self.find(obj_flags,line)
        ref_ind = [(x[0],x[1].replace('(','').replace(')','')) for x in ref_ind if x[1].replace('(','').replace(')','')]
        ref_ind = [(x[0],x[1]) for x in ref_ind if '@' in x[1]]
        return ref_ind