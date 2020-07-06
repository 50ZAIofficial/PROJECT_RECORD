################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

CG_TOOL_ROOT := D:/ti/ccs/tools/compiler/ti-cgt-c2000_18.12.1.LTS

GEN_OPTS__FLAG := 
GEN_CMDS__FLAG := 

ORDERED_OBJS += \
"./main.obj" \
"./include/DSP2833x_ADC_cal.obj" \
"./include/DSP2833x_CodeStartBranch.obj" \
"./include/DSP2833x_DefaultIsr.obj" \
"./include/DSP2833x_GlobalVariableDefs.obj" \
"./include/DSP2833x_Gpio.obj" \
"./include/DSP2833x_PieCtrl.obj" \
"./include/DSP2833x_PieVect.obj" \
"./include/DSP2833x_SysCtrl.obj" \
"./include/DSP2833x_usDelay.obj" \
"../28335_RAM_lnk.cmd" \
"../include/DSP2833x_Headers_nonBIOS.cmd" \
"../include/IQmath.lib" \
$(GEN_CMDS__FLAG) \
-llibc.a \

-include ../makefile.init

RM := DEL /F
RMDIR := RMDIR /S/Q

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir_vars.mk
-include include/subdir_vars.mk
-include subdir_rules.mk
-include include/subdir_rules.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C55_DEPS)),)
-include $(C55_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(S67_DEPS)),)
-include $(S67_DEPS)
endif
ifneq ($(strip $(S62_DEPS)),)
-include $(S62_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(OPT_DEPS)),)
-include $(OPT_DEPS)
endif
ifneq ($(strip $(C??_DEPS)),)
-include $(C??_DEPS)
endif
ifneq ($(strip $(ASM_UPPER_DEPS)),)
-include $(ASM_UPPER_DEPS)
endif
ifneq ($(strip $(S??_DEPS)),)
-include $(S??_DEPS)
endif
ifneq ($(strip $(C64_DEPS)),)
-include $(C64_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(S64_DEPS)),)
-include $(S64_DEPS)
endif
ifneq ($(strip $(INO_DEPS)),)
-include $(INO_DEPS)
endif
ifneq ($(strip $(CLA_DEPS)),)
-include $(CLA_DEPS)
endif
ifneq ($(strip $(S55_DEPS)),)
-include $(S55_DEPS)
endif
ifneq ($(strip $(SV7A_DEPS)),)
-include $(SV7A_DEPS)
endif
ifneq ($(strip $(C62_DEPS)),)
-include $(C62_DEPS)
endif
ifneq ($(strip $(C67_DEPS)),)
-include $(C67_DEPS)
endif
ifneq ($(strip $(PDE_DEPS)),)
-include $(PDE_DEPS)
endif
ifneq ($(strip $(K_DEPS)),)
-include $(K_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C43_DEPS)),)
-include $(C43_DEPS)
endif
ifneq ($(strip $(S43_DEPS)),)
-include $(S43_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(SA_DEPS)),)
-include $(SA_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXE_OUTPUTS += \
28335PWMmod.out \

EXE_OUTPUTS__QUOTED += \
"28335PWMmod.out" \

BIN_OUTPUTS += \
28335PWMmod.hex \

BIN_OUTPUTS__QUOTED += \
"28335PWMmod.hex" \


# All Target
all: $(OBJS) $(CMD_SRCS) $(LIB_SRCS) $(GEN_CMDS)
	@$(MAKE) --no-print-directory -Onone "28335PWMmod.out"

# Tool invocations
28335PWMmod.out: $(OBJS) $(CMD_SRCS) $(LIB_SRCS) $(GEN_CMDS)
	@echo 'Building target: "$@"'
	@echo 'Invoking: C2000 Linker'
	"D:/ti/ccs/tools/compiler/ti-cgt-c2000_18.12.1.LTS/bin/cl2000" -v28 -ml -mt --float_support=fpu32 --advice:performance=all -g --diag_warning=225 --diag_wrap=off --display_error_number --abi=coffabi -z -m"28335PWMmod.map" --stack_size=0x300 --warn_sections -i"D:/ti/ccs/tools/compiler/ti-cgt-c2000_18.12.1.LTS/lib" -i"D:/ti/ccs/tools/compiler/ti-cgt-c2000_18.12.1.LTS/include" --reread_libs --diag_wrap=off --display_error_number --xml_link_info="28335PWMmod_linkInfo.xml" --rom_model -o "28335PWMmod.out" $(ORDERED_OBJS)
	@echo 'Finished building target: "$@"'
	@echo ' '

28335PWMmod.hex: $(EXE_OUTPUTS)
	@echo 'Building files: $(strip $(EXE_OUTPUTS__QUOTED))'
	@echo 'Invoking: C2000 Hex Utility'
	"D:/ti/ccs/tools/compiler/ti-cgt-c2000_18.12.1.LTS/bin/hex2000"  -o "28335PWMmod.hex" $(EXE_OUTPUTS__QUOTED)
	@echo 'Finished building: $(strip $(EXE_OUTPUTS__QUOTED))'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(BIN_OUTPUTS__QUOTED)$(EXE_OUTPUTS__QUOTED)
	-$(RM) "main.obj" "include\DSP2833x_ADC_cal.obj" "include\DSP2833x_CodeStartBranch.obj" "include\DSP2833x_DefaultIsr.obj" "include\DSP2833x_GlobalVariableDefs.obj" "include\DSP2833x_Gpio.obj" "include\DSP2833x_PieCtrl.obj" "include\DSP2833x_PieVect.obj" "include\DSP2833x_SysCtrl.obj" "include\DSP2833x_usDelay.obj" 
	-$(RM) "main.d" "include\DSP2833x_DefaultIsr.d" "include\DSP2833x_GlobalVariableDefs.d" "include\DSP2833x_Gpio.d" "include\DSP2833x_PieCtrl.d" "include\DSP2833x_PieVect.d" "include\DSP2833x_SysCtrl.d" 
	-$(RM) "include\DSP2833x_ADC_cal.d" "include\DSP2833x_CodeStartBranch.d" "include\DSP2833x_usDelay.d" 
	-@echo 'Finished clean'
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets

