#!/bin/bash

# Function to send notifications
send_notification() {
    case "$1" in
        "Critical - Long Text") notify-send -u critical "Critical Urgency" "This is a long critical-urgency notification with extended text." ;;
        "Critical - Short Text") notify-send -u critical "Critical Urgency" "This is a short critical-urgency notification." ;;
        "Critical - With Icon") notify-send -u critical -i dialog-warning "Critical Urgency" "This notification has an icon." ;;
        "Low - Long Text") notify-send -u low "Low Urgency" "This is a longer low-urgency notification. It contains more text to test wrapping." ;;
        "Low - Short Text") notify-send -u low "Low Urgency" "This is a short low-urgency notification." ;;
        "Normal - Long Text") notify-send -u normal "Normal Urgency" "This is a longer normal-urgency notification to check the appearance." ;;
        "Normal - Short Text") notify-send -u normal "Normal Urgency" "This is a short normal-urgency notification." ;;
        "Normal - With Icon") notify-send -u normal -i face-smile "Normal Urgency" "This is a notification with an icon." ;;
        "Run All") 
            notify-send -u low "Low Urgency" "This is a short low-urgency notification."
            notify-send -u low "Low Urgency" "This is a longer low-urgency notification. It contains more text to test wrapping."
            notify-send -u normal "Normal Urgency" "This is a short normal-urgency notification."
            notify-send -u normal "Normal Urgency" "This is a longer normal-urgency notification to check the appearance."
            notify-send -u critical "Critical Urgency" "This is a short critical-urgency notification."
            notify-send -u critical "Critical Urgency" "This is a long critical-urgency notification with extended text."
            notify-send -u normal -i face-smile "Normal Urgency" "This is a notification with an icon."
            notify-send -u critical -i dialog-warning "Critical Urgency" "This notification has an icon."
            ;;
        *) echo "Invalid option: $1" ;;
    esac
}

# Sorted Notification Options
OPTIONS=(
    "Critical - Long Text"
    "Critical - Short Text"
    "Critical - With Icon"
    "Low - Long Text"
    "Low - Short Text"
    "Normal - Long Text"
    "Normal - Short Text"
    "Normal - With Icon"
    "Run All"
)

# Run fzf menu
CHOICES=$(printf "%s\n" "${OPTIONS[@]}" | fzf --multi --height=40% --border \
    --prompt="Select Notifications: " \
    --color=fg:#f8f8f2,bg:#282a36,hl:#bd93f9 \
    --color=fg+:#f8f8f2,bg+:#44475a,hl+:#bd93f9 \
    --color=info:#ffb86c,prompt:#50fa7b,pointer:#ff79c6 \
    --color=marker:#ff79c6,spinner:#ffb86c,header:#6272a4)

# Handle multi-word selections correctly
IFS=$'\n'
for choice in $CHOICES; do
    send_notification "$choice"
done
unset IFS
