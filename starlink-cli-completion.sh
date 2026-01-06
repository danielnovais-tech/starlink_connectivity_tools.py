#!/bin/bash
# Bash completion script for starlink-cli
# Install: cp starlink-cli-completion.sh /etc/bash_completion.d/
# Or source it: source starlink-cli-completion.sh

_starlink_cli_completions()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    local commands="status monitor report reboot thresholds export connection"
    
    # Options
    local opts="--host --interval --duration --hours --output --format --log-level --log-file --version --help"
    
    # Complete commands
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi
    
    # Complete options
    case "${prev}" in
        --format)
            COMPREPLY=( $(compgen -W "json csv" -- ${cur}) )
            return 0
            ;;
        --log-level)
            COMPREPLY=( $(compgen -W "DEBUG INFO WARNING ERROR CRITICAL" -- ${cur}) )
            return 0
            ;;
        --output|--log-file)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        --host)
            COMPREPLY=( $(compgen -W "192.168.100.1" -- ${cur}) )
            return 0
            ;;
        --interval|--duration|--hours)
            # No completion for numbers
            return 0
            ;;
    esac
    
    # Complete with options
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _starlink_cli_completions starlink-cli
complete -F _starlink_cli_completions python3\ cli/starlink_cli.py
