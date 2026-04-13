--This script is ahh and not neccesary but I will keep it for history only xD

--[[
    local url = arg[1]

    local function validate_url(url)
        local isHttp = false
        local hasDomain = false
        local httpPattern = "^https://"
        if string.sub(url, 1, #httpPattern) == httpPattern then
            isHttp = true
        else
            print("invalid:URL must start with 'https://'")
            return
        end
        local host_and_path = string.sub(url, #httpPattern)
        local host = string.match(host_and_path, "^([^/]+)")

        if not host then
            print("invalid:URL does not contain host")
            return
        end
        -- regex: 
        -- ^[a-zA-Z0-9.-]+  -> starts with approved symbols
        -- %.[a-zA-Z]{2,}$  -> ends with . and minimum of 2 symbols after

        if string.match(host, "^[a-zA-Z0-9]([a-zA-Z0-9%-]*[a-zA-Z0-9])?%.[a-zA-Z0-9]([a-zA-Z0-9%-]*[a-zA-Z0-9])?%.[a-zA-Z]{2,}$") then
            hasDomain = true
        else
            print("invalid:URL does not contain domain")
            return
        end

        if hasDomain and isHttp then
            print("valid:")
            return
        end
    end

    validate_url(url)
]]