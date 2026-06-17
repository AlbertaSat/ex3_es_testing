#!/bin/bash

# Define test constants
TEST_NUMBER=9
TEST_DESCRIPTION="gpio"

# GPIO Names and their respective expected pull configurations
# Format: ["GPIO_NAME"]="pull_type"
declare -A GPIOS=(
    ["UHF_UART_RX"]="none"
    ["SBAND_TR"]="none"
    ["STACK_SBAND_n_RESET"]="none"
    ["Q7_DFGMKnifeEN"]="down"
    ["Q7_StarboardKnifeEN"]="down"
    ["SwitchDeployable_S"]="none"
    ["SwitchDeployable_P"]="none"
    ["Starboard_IR_Sens"]="down"
    ["SP_nAlert"]="none"
    ["SP_SHDN"]="none"
    ["GPS_nAlert"]="none"
    ["GPS_SHDN"]="none"
    ["Port_IR_Sens"]="down"
    ["STACK_SBAND_STX_EN"]="down"
    ["DFGM_IR_Sens"]="down"
    ["TS_Alert"]="none"
    ["TS_RS"]="down"
    ["GPS_RSTN"]="up"
    ["HUB_RESET_L"]="up"
    ["HUB_HS_IND"]="down"
    ["Q7_PortKnifeEN"]="down"
    ["CAN_EN"]="up"
    ["CAN_RS"]="down"
    ["HUB_SETUP_IND"]="down"
)

# Ordered list of GPIO keys to ensure deterministic iteration order.
# Iterate over this array instead of the associative array keys.
GPIOS_ORDER=(
    "SBAND_TR"
    "STACK_SBAND_n_RESET"
    "Q7_DFGMKnifeEN"
    "Q7_StarboardKnifeEN"
    "Q7_PortKnifeEN"
    "SwitchDeployable_S"
    "SwitchDeployable_P"
    "Starboard_IR_Sens"
    "SP_nAlert"
    "SP_SHDN"
    "GPS_nAlert"
    "GPS_SHDN"
    "Port_IR_Sens"
    "STACK_SBAND_STX_EN"
    "DFGM_IR_Sens"
    "TS_Alert"
    "TS_RS"
    "GPS_RSTN"
    "UHF_UART_RX"
    "HUB_RESET_L"
    "HUB_HS_IND"
    "CAN_EN"
    "CAN_RS"
    "HUB_SETUP_IND"
)

# Tracks failed GPIO names
FAILED_GPIOS=()

setup() {
    echo "${TEST_DESCRIPTION}_${TEST_NUMBER} setup"
}

teardown() {
    echo "${TEST_DESCRIPTION}_${TEST_NUMBER} teardown"
}

run_test() {
    echo "${TEST_DESCRIPTION}_${TEST_NUMBER} test"

    # Iterate over the ordered keys to ensure deterministic order
    for gpio in "${GPIOS_ORDER[@]}"; do
        pull="${GPIOS[$gpio]}"
        
        # -------------------------------------------------------------
        # LOW Test
        # -------------------------------------------------------------
        gpioset $(gpiofind "$gpio")=0
        
        read -p "Is $gpio is LOW on the DMM? [y/n]: " response
        if [[ "${response,,}" != "y" ]]; then
            echo "GPIO $gpio LOW test failed, user indicated value was not LOW"
            FAILED_GPIOS+=("$gpio")
        else
            echo "GPIO $gpio LOW test passed, user indicated value was LOW"
        fi

        # -------------------------------------------------------------
        # HIGH Test
        # -------------------------------------------------------------
        gpioset $(gpiofind "$gpio")=1
        
        read -p "Is $gpio is HIGH on the DMM? [y/n]: " response
        if [[ "${response,,}" != "y" ]]; then
            echo "GPIO $gpio HIGH test failed, user indicated value was not HIGH"
            FAILED_GPIOS+=("$gpio")
        else
            echo "GPIO $gpio HIGH test passed, user indicated value was HIGH"
        fi

        # -------------------------------------------------------------
        # Reset GPIO to Input (gpioget releases ownership of line)
        # -------------------------------------------------------------
        gpioget $(gpiofind "$gpio") > /dev/null 2>&1

        # Wait a moment for the line state to stabilize after releasing ownership
        sleep 0.5

        if [[ "$pull" == "none" ]]; then
            continue
        fi

        # -------------------------------------------------------------
        # Pull Up / Pull Down Test
        # -------------------------------------------------------------
        out=$(gpioget $(gpiofind "$gpio") 2>/dev/null)

        if [[ "$pull" == "up" ]]; then
            expected="1"
            expected_text="HIGH"
        elif [[ "$pull" == "down" ]]; then    
            expected="0"
            expected_text="LOW"
        else
            echo "Invalid pull value $pull for GPIO $gpio, skipping pull test"
            continue
        fi

        # Strip any surrounding whitespace from output
        out_trimmed=$(echo "$out" | tr -d '[:space:]')

        if [[ "$out_trimmed" == "$expected" ]]; then 
            echo "GPIO $gpio pull $pull test passed, value $out_trimmed matches expected $expected"
        else
            echo "GPIO $gpio pull $pull test failed, value $out_trimmed does not match expected $expected"
            FAILED_GPIOS+=("$gpio")
        fi

        # Prompt user to verify pull state on DMM
        read -p "Is $gpio $expected_text on the DMM due to the pull $pull? [y/n]: " response
        if [[ "${response,,}" != "y" ]]; then
            echo "GPIO $gpio pull $pull test failed, user indicated value was not $expected_text"
            FAILED_GPIOS+=("$gpio")
        else
            echo "GPIO $gpio pull $pull test passed, user indicated value was $expected_text"
        fi
    done

    # -------------------------------------------------------------
    # Evaluation & Results
    # -------------------------------------------------------------
    if [ ${#FAILED_GPIOS[@]} -ne 0 ]; then
        # Join array elements by comma
        failed_list=$(IFS=,; echo "${FAILED_GPIOS[*]}")
        echo "GPIO pull tests failed for the following GPIOs: $failed_list"
        return 1 # Corresponds to PhaseResult.FAIL_AND_CONTINUE / Non-zero exit status
    else
        echo "GPIO pull tests passed for all GPIOs"
        return 0
    fi
}

# --- Script Execution ---
setup
run_test
test_result=$?
teardown

# Exit script with the test result code
exit $test_result
