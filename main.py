import numpy as np
from ReadAssemblyFile import AssemblyReader

MEMORY = {}
MEMORY_SIZE = 4096
MAX_INST_ITER = 10_000
ZERO_FLAG_REGISTER = 0
GENERAL_REGISTER_SIZE = 4
PC = 0
REGISTERS = [0]*GENERAL_REGISTER_SIZE
instruction_list = ["inc", "not", "mov", "sub",
                    "or", "and", "xor", "ldi", "ld",
                    "add", "dec", "jz", "jmp", "st"]


def main():
    AR = AssemblyReader(assembly_filename="./Inputs/AssemblyCode_1.txt",
                        instruction_list=instruction_list)
    global MEMORY
    MEMORY = AR.data_dict.copy()
    InstructionOperator(AR=AR)
    PrintMachineState()


def PrintMachineState():
    global ZERO_FLAG_REGISTER, REGISTERS, MEMORY, PC
    print(f"Registers:")
    print(f"\tProgram Counter: {PC}")
    print(f"\tZero Flag Register: {ZERO_FLAG_REGISTER}")
    for i in range(len(REGISTERS)):
        print(f"\tReg{i}: {REGISTERS[i]}")
    print(f"Memory:")
    for key, val in MEMORY.items():
        print(f"\tMemory Location #{key}: {val}")
    print()


def GetFromDict(dict_to_get, key):
    if key in dict_to_get:
        return dict_to_get[key]
    else:
        dict_to_get[key] = 0
        return dict_to_get[key]


def InstructionOperator(AR):
    iter_no = 0
    program_counter_old = 0
    program_counter_new = 1
    while (iter_no < MAX_INST_ITER):
        iter_no += 1
        instruction_type = AR.code_rows[program_counter_old].split()[0]
        if instruction_type not in instruction_list:
            raise Exception(
                "Wrong instruction type: {instruction_type} not found.")  # ERROR
        program_counter_new = RunSingleInstruction(instruction_memory=AR.code_rows,
                                                   program_counter=program_counter_old,
                                                   label_dict=AR.label_dict)
        if program_counter_old == program_counter_new:
            global PC
            PC = program_counter_old
            break
        program_counter_old = program_counter_new
    else:
        raise Exception(
            "Maximum instruction iteration count has been reached.")
    print(f"\n-----Program execution ended-----\nIteration Count: {iter_no}")


def CheckLengthInstruction(instruction_split):
    instruction_type = instruction_split[0]

    if (instruction_type in ["ldi", "ld", "st", "mov", "not"]):
        if (len(instruction_split) != 3):
            raise Exception("ERROR")
    elif (instruction_type in ["inc", "dec", "jmp", "jz"]):
        if (len(instruction_split) != 2):
            raise Exception("ERROR")
    elif (instruction_type in ["xor", "sub", "and", "add", "or", ""]):
        if (len(instruction_split) != 4):
            raise Exception("ERROR")


def RunSingleInstruction(instruction_memory, program_counter, label_dict):
    instruction_split = instruction_memory[program_counter].split()
    instruction_type = instruction_split[0]
    CheckLengthInstruction(instruction_split=instruction_split)
    global ZERO_FLAG_REGISTER, REGISTERS, MEMORY
    if (instruction_type == "ldi"):
        store_register = instruction_split[1]
        store_value = instruction_split[2]
        if (store_value in MEMORY):
            try:
                store_register = int(store_register)
                store_value = str(store_value)
            except ValueError:
                raise Exception(
                    f"Wrong type for {store_register} or {store_value}")
        else:
            try:
                store_register = int(store_register)
                store_value = int(store_value)
            except ValueError:
                raise Exception(
                    f"Wrong type for {store_register} or {store_value}")
        REGISTERS[store_register] = store_value
        return program_counter + 1
    elif (instruction_type == "not"):
        source_register = instruction_split[1]
        dest_register = instruction_split[0]
        try:
            dest_register = int(dest_register)
            source_register = int(source_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source_register} or {dest_register}")
        alu_res = ~REGISTERS[source_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "inc"):
        store_register = instruction_split[1]
        try:
            store_register = int(store_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {store_register}")
        alu_res = REGISTERS[store_register] + 1
        REGISTERS[store_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "dec"):
        store_register = instruction_split[1]
        try:
            store_register = int(store_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {store_register}")
        alu_res = REGISTERS[store_register] - 1
        REGISTERS[store_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "mov"):
        source_register = instruction_split[1]
        dest_register = instruction_split[0]
        try:
            dest_register = int(dest_register)
            source_register = int(source_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source_register} or {dest_register}")
        alu_res = REGISTERS[source_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "sub"):
        source1_register = instruction_split[2]
        source2_register = instruction_split[3]
        dest_register = instruction_split[1]
        try:
            source1_register = int(source1_register)
            source2_register = int(source2_register)
            dest_register = int(dest_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source1_register} or {source2_register} or {dest_register}")
        alu_res = REGISTERS[source1_register] - \
            REGISTERS[source2_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "or"):
        source1_register = instruction_split[2]
        source2_register = instruction_split[3]
        dest_register = instruction_split[1]
        try:
            source1_register = int(source1_register)
            source2_register = int(source2_register)
            dest_register = int(dest_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source1_register} or {source2_register} or {dest_register}")
        alu_res = REGISTERS[source1_register] | \
            REGISTERS[source2_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "and"):
        source1_register = instruction_split[2]
        source2_register = instruction_split[3]
        dest_register = instruction_split[1]
        try:
            source1_register = int(source1_register)
            source2_register = int(source2_register)
            dest_register = int(dest_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source1_register} or {source2_register} or {dest_register}")
        alu_res = REGISTERS[source1_register] & \
            REGISTERS[source2_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "xor"):
        source1_register = instruction_split[2]
        source2_register = instruction_split[3]
        dest_register = instruction_split[1]
        try:
            source1_register = int(source1_register)
            source2_register = int(source2_register)
            dest_register = int(dest_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source1_register} or {source2_register} or {dest_register}")
        alu_res = REGISTERS[source1_register] ^ \
            REGISTERS[source2_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "add"):
        source1_register = instruction_split[2]
        source2_register = instruction_split[3]
        dest_register = instruction_split[1]
        try:
            source1_register = int(source1_register)
            source2_register = int(source2_register)
            dest_register = int(dest_register)
        except ValueError:
            raise Exception(
                f"Wrong type for {source1_register} or {source2_register} or {dest_register}")
        alu_res = REGISTERS[source1_register] + \
            REGISTERS[source2_register]
        REGISTERS[dest_register] = alu_res
        ZERO_FLAG_REGISTER = alu_res == 0
        return program_counter + 1
    elif (instruction_type == "jz"):
        label = instruction_split[1]
        if (label not in label_dict):
            raise Exception(f"There is no {label} as label.")
        if (ZERO_FLAG_REGISTER):
            program_counter = label_dict[label]
            return program_counter
        return program_counter + 1
    elif (instruction_type == "jmp"):
        label = instruction_split[1]
        if (label not in label_dict):
            raise Exception(f"There is no {label} as label.")
        program_counter = label_dict[label]
        return program_counter
    elif (instruction_type == "ld"):

        dest_register = instruction_split[1]
        source_register = instruction_split[2]
        try:
            dest_register = int(dest_register)
            source_register = int(source_register)
            source_address = str(REGISTERS[source_register])
            REGISTERS[dest_register] = int(
                GetFromDict(MEMORY, source_address))
        except ValueError:
            raise Exception(
                f"Wrong type for {dest_register} or {source_register}.")
        return program_counter + 1
    elif (instruction_type == "st"):
        stored_register = instruction_split[1]
        dest_register = instruction_split[2]
        try:
            dest_register = int(dest_register)
            dest_address = str(REGISTERS[dest_register])
            stored_register = int(stored_register)
            MEMORY[dest_address] = REGISTERS[stored_register]
        except ValueError:
            raise Exception(
                f"Wrong type for {dest_register} or {stored_register}.")
        return program_counter + 1
    else:
        raise Exception(f"Wrong instruction type: {instruction_type}")


if __name__ == "__main__":
    main()
    exit()
