#This file contains all the required prompts that will be used in Response Generation.

summarization_prompt = '''Your goal is to create a compelling and engaging summary of the following sales pitch by focusing on the key features and benefits of the product. Present your pitch in concise bullet points to captivate your audience and highlight the unique selling points. Remember to emphasize the value proposition and address any pain points your target customers may have. Keep the summary crisp, concise, and persuasive to leave a lasting impact on potential buyers.\n 
Here is the provided pitch for which you have to create the summary.\n
\n.........\n
pitch : {pitch_gen}
\n.........\n
summary : '''


recommend_template="These are the ABSLI product details listed with three backticks ```{input_query}```.These are customer details entry age group of customer= '{age_group}', annual income ='{income_group}', goal= '{goal}', risk= '{risk}' and profile= '{profile}' .With not more than 250 words your goal is to recommend a best ABSLI product plan.Please make sure to compare every detail of customer with all products eligibily criteria mentioned previously then only recommend the product.For example, if the maximum age of entry for a product is 55 years and the person’s age is 65, which is above the entry limit, then this product should not be recommended. Instead, another product that is suitable for their age should be chosen.Give detailed explanation of why you recommend that product for the customer by comparing with customer details.Please Provide response in an organized way.Please make sure you don't repeat the same point again.Response should not include other details only provide recommended product details.Your response should be clear and informative.Don't provide additional information from your knowledge base.\n Take this as an example: \n,{example_learn}\n your task is to make sure that the each response should be the same structure as the example provided.\n Take this as an example: \n,{example_learn}\n your task is to make sure that the each response should be the same structure as the example provided."

history_context_prompt = '''Your task is to take into consideration two things, one is the chat history that has happend\
        between the User and AI and other is the question. Now you need to modify the question if only it is \
        needed according to chat history and generate  a new question that can searched upon. You have to handle\
        follow up questions and take into considerations the previous responses of the AI if necessary. \
        Do not assume abbrivations based on your knowledge return abbrivations as it is in question.\
        If the question is not related to the previous responses then output the same question as inputted.\
        If you are not confident on whether the question is related to previous responses, then output the same question.
        Example 1:
        ------------
        Chat History:
        User: When is MG University established?
        AI: 1998

        Given question: then what about Rao University?
        Rephrased question: When is Rao University established?
        ------------

        Example 2:
        ------------
        Chat History:
        User: When is the Republic day of India?
        AI: January 26

        Given question: Who is Pawan Kalyan?
        Rephrased question: Who is Pawan Kalyan?
        ------------
        '''