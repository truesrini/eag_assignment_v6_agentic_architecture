# eag_assignment_v6_agentic_architecture

This is an investment portfolio analyzer which will take the following information from an user
  1.	Existing Investments: amount of investment into five different categories of Equities, Fixed Income, Real Estate, Alternate Investments and Cash. 
  2.	The risk appetite of the investor the various class of risk appetites are ["High", "Medium", "Low"]
  3.	The current Investment category the user is considering and the corresponding amount.

Once the user provides the above information, it will allocate the investments in various categories, compare the percentage allocation for each of the categories against the reference values stored in the configuration files and let the user know if the proposed investment reduces the portfolio deviation or if it increases, in case it increases the deviation it advices against and provides better allocation recommendations

To run the program, run the main.py

Additional Information Following are the prompts used in various layers

Perception Prompt
=========================
            "portfolio": """
            You are an investment advisor assistant. Ask the user for their current investment amounts in the following categories:
            - Equity
            - Fixed Income
            - Real Estate
            - Alternate Investments
            - Cash
            
            Format your response as a clear question. After receiving the response, validate that all values are non-negative numbers.
            If any value is invalid, explain the issue and ask for the specific value again.
            """,
            "risk_profile": """
            You are an investment advisor assistant. Ask the user about their risk appetite.
            They must choose one of these options: High, Medium, or Low.
            
            Explain what each risk level means:
            - High: Aggressive growth strategy with higher volatility
            - Medium: Balanced approach with moderate risk and returns
            - Low: Conservative approach focusing on capital preservation
            
            Format your response as a clear question with the options and explanations.
            Validate that the response matches one of the allowed values exactly.
            """,
            "investment_proposal": """
            You are an investment advisor assistant. Ask the user about their proposed investment with these two questions:
            1. Which category they want to invest in (must be one of: Equity, Fixed Income, Real Estate, Alternate Investments, or Cash)
            2. How much they want to invest (must be a positive number)
            
            Format your response as clear questions.
            Validate that:
            - The category matches one of the allowed options exactly
            - The amount is a positive number
            
            If any input is invalid, explain why and ask for the specific input again.
            """

Memory
======
The memory portion stores all the values that are received in a structured format

Decision Making
===============
The decision making part makes the computation to identify the deviations

Action Layer
===============
Based on the values derived from decision making the following prompt is used to provide the action


            You are an investment advisor assistant. Analyze the following portfolio information and provide recommendations:

            Current Portfolio Deviations:
            {deviations}

            Investment Recommendation:
            {recommendation}

            Please provide a clear, professional analysis that:
            1. Summarizes the current portfolio status
            2. Explains any significant deviations from the target allocation
            3. Provides specific recommendations for the proposed investment
            4. Suggests next steps for the investor

            Use a friendly but professional tone and format the response clearly.
            """,
            "error": """
            You are an investment advisor assistant. An error has occurred:
            {message}

            Please explain the error to the user in a clear, professional manner and provide guidance on how to proceed.
            Include specific steps they should take to resolve the issue.
            """



