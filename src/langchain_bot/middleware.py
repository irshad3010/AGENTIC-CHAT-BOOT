
from datetime import datetime

from langchain.agents.middleware import (
    wrap_model_call,
    wrap_tool_call,
)


# --------------------------------------------------
# 1. Timestamp helper
# --------------------------------------------------

def _ts():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# --------------------------------------------------
# 2. Model logging middleware
# --------------------------------------------------

@wrap_model_call
def model_logging_middleware(request, handler):

    messages = request.messages

    message_count = len(messages)

    last_message = (
        messages[-1]
        if messages
        else None
    )

    preview = ""

    if last_message:

        preview = str(
            last_message.content
        )[:150]

    print(
        f"\n[{_ts()}] MODEL REQUEST"
    )

    print(
        f"Message count: {message_count}"
    )

    print(
        f"Last message: {preview}"
    )

    try:

        # Synchronous handler call
        response = handler(request)

        response_messages = getattr(
            response,
            "messages",
            []
        )

        if response_messages:

            last_response = response_messages[-1]

            response_preview = str(
                last_response.content
            )[:200]

            print(
                f"\n[{_ts()}] MODEL RESPONSE"
            )

            print(
                f"Response: {response_preview}"
            )

            tool_calls = getattr(
                last_response,
                "tool_calls",
                []
            )

            if tool_calls:

                print(
                    f"[{_ts()}] TOOL CALLS: {tool_calls}"
                )

        return response

    except Exception as e:

        print(
            f"\n[{_ts()}] MODEL ERROR: {e}"
        )

        raise


# --------------------------------------------------
# 3. Tool logging middleware
# --------------------------------------------------

@wrap_tool_call
def tool_logging_middleware(request, handler):

    tool_call = getattr(
        request,
        "tool_call",
        {}
    )

    tool_name = tool_call.get(
        "name",
        "unknown"
    )

    tool_args = tool_call.get(
        "args",
        {}
    )

    print(
        f"\n[{_ts()}] TOOL START"
    )

    print(
        f"Tool: {tool_name}"
    )

    print(
        f"Arguments: {tool_args}"
    )

    try:

        # Synchronous handler call
        result = handler(request)

        print(
            f"[{_ts()}] TOOL SUCCESS: {tool_name}"
        )

        return result

    except Exception as e:

        print(
            f"[{_ts()}] TOOL ERROR: {tool_name} - {e}"
        )

        raise


# --------------------------------------------------
# 4. Export middleware
# --------------------------------------------------

def get_logging_middleware():

    return [
        model_logging_middleware,
        tool_logging_middleware
    ]


__all__ = [
    "model_logging_middleware",
    "tool_logging_middleware",
    "get_logging_middleware"
]
