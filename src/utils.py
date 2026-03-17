"""
File: utils.py
Date: June 21, 2023

Description:
This file contains utility functions for the sales pitch and document question answering service. It provides a collection of helper functions to support various tasks related to sales pitch generation, recommendation, summarization and document question and answers.

The main utility functions included in this file are:

- Sales-Copilot class:  sales pitch generation, recommendation, summarization with GPT.
- Prompt : Creation of prompt based on history or question context
- Answer generation: Documetion question answering based on faiss and GPT.


Note: This file may have dependencies on external libraries or modules. Please refer to the import statements for the required dependencies.

Functions:
- recommendation(self, input_query_recommend, plan_details)
- pitchgen(self, input_query, pitch_len)
- summarize(self, pitch_gen)
- num_tokens_from_messages_docs(messages, encoding)
- create_prompt(text,question)
- get_embeddings(file_name)
- qa(text: str, questions)
- multiqa_using_gpt3(question)
- qa_driver(query,history)

"""
# Importing required modules 
from src.dependencies import *
from config.config import *
    
with open("embeddings/ABSLI_qa_Embeddings.pkl", "rb") as f:
    embeddings_plan1 = pickle.load(f)


encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
token_limit= 4096
max_response_token = 500


model_name = 'gpt-3.5-turbo'
model = OpenAI(model_name=model_name,engine="Absligpt35-SC",n=1,temperature=0.9,verbose=True,api_version="2023-03-15-preview",api_base="https://openaiabsli-sc.openai.azure.com/",api_key="e743d453bbfd4470bfeee7e695350b44",api_type="Azure")

class SALES_Copilot:
    @staticmethod
    def __init__():
        SALES_Copilot.character = "You are the experienced senior sales person working as a sales executive in Aditya Birla\
         Sun Life Insurance firm. You possess in-depth knowledge of various insurance products and their benefits."      
        SALES_Copilot.engine = "Absligpt35-SC"
        SALES_Copilot.temperature = 0
        SALES_Copilot.max_tokens = 1024
        SALES_Copilot.n = 1
        SALES_Copilot.encoding_ = tiktoken.encoding_for_model("gpt-3.5-turbo")
        SALES_Copilot.token_limit= 4096
        SALES_Copilot.max_response_token = 500
        SALES_Copilot.model = OpenAI(model_name="gpt-3.5-turbo",engine="Absligpt35-SC",n=1,temperature=0.9,verbose=True,api_version="2023-03-15-preview",api_base="https://openaiabsli-sc.openai.azure.com/",api_key="e743d453bbfd4470bfeee7e695350b44",api_type="Azure")

        
    @staticmethod
    def summarize(pitch_gen: str) -> str:
        """
        Summarize a generated pitch.

        Args:
            pitch_gen (str): The generated pitch that needs to be summarized.

        Returns:
           summarize_pitch (str): A summary of the generated pitch.
            
        """
        
        prompt =  summarization_prompt.format(pitch_gen = pitch_gen)
        print(prompt)
        try:
            response = openai.Completion.create(
                engine = SALES_Copilot.engine,
                prompt = prompt,
                max_tokens=SALES_Copilot.max_tokens,
                n=SALES_Copilot.n,
                stop='\n\n',
                 temperature=SALES_Copilot.temperature
                )
        except Exception as e:
            print(e)
        summ_pitch = response["choices"][0]["text"]  
        print(summ_pitch)
        return summ_pitch

    @staticmethod
    def qa_chat(query, session_id,history):
        if(query=='clear'):
            if(session_id in history):
                history.pop(session_id)
                response = jsonify({'response': 'Session history has been cleared!'})
                response.status_code = 200
                return response
            response = jsonify({'response': 'There was no previous session allocated for this session id.'})
            response.status_code = 200
            return response
        if(session_id not in history):
            history[session_id] = copy.deepcopy(messages)

        if(query=='restart'):
            history[session_id] = copy.deepcopy(messages)
            response = jsonify({'response': 'History has been cleared successfully!'})
            response.status_code = 200
            return response
        
        else:
            word_list = re.split(r"[-;,.\s]\s*", query.lower())

            if('pitch' in word_list):
                response = {'response': 'Intent: Sales Pitch'}
                return response
            
            elif('recommend' in word_list or 'recommendation' in word_list or 'suggest' in word_list or 'suggestion' in word_list):
                response = {'response': 'Intent: Recommendation'}
                return response
            
            elif('summarize' in word_list):
                response = {'response': 'Summarization'}
                return response
            
            else:
                print('Inside QA')
                
                conv_history_tokens = sales_copilot.num_tokens_from_messages_docs(docs_history)

                if(conv_history_tokens>=token_limit):
                    response = jsonify({'response' :f'Max token limit reached. You used {conv_history_tokens} tokens.'})
                    return response
                    
                elif(conv_history_tokens+max_response_tokens >= token_limit):
                    response = jsonify({'response' :f'Generating this answer would cause the token limit to be breached and may\
                    generate partial answers. You used {conv_history_tokens} tokens.'})
                    return response
                
                else:
                    try:
                        res,search_query = SALES_Copilot.qa_driver(query,history[session_id],history_context_prompt,model)
                        history[session_id].append(HumanMessage(content=search_query))
                        history[session_id].append(AIMessage(content=str(res)))
                        response = {'response': str(res)}
                        print(res)
                        return str(res)
                    except Exception as e:
                        return {f"Error {e} occured."}
    
    @staticmethod
    def recommendation(age_group,goal,income_group,risk,profile,example_recommend,model,recommend_template):
        blob_client = container_client.get_blob_client('ABSLI_recommendation_summary.json')
        blob_data = blob_client.download_blob().readall()
        json_data = json.loads(blob_data)
        json_data = json.dumps(json_data)
        plan_details = json_data
        plan_details=json.loads(plan_details)           

        plan_jsons=plan_details['Plan_metadata']['metadata']

        example_learn = example_recommend
        
        prompt_review = PromptTemplate.from_template(
                        template=recommend_template
                )
        recommed_chain = LLMChain(llm=model, prompt=prompt_review, output_key="Recommend_pitch")

        overall_chain = SequentialChain(
        chains=[recommed_chain],
        input_variables=["age_group","income_group","goal","plan","input_query","risk","example_learn","profile"],
        output_variables=["Recommend_pitch"],
            )
        #Income Filter
        income_plans = income_check(income_group,plan_jsons)

        ## Checking for NA's in the mentioned parameters
        try:
            income_plans=[plan for plan in income_plans if sales_copilot.sales_pitch_dict(plan,goal,profile)!="Na"]
        except:
            pass
        ## Age Filter
        income_plan_details=[details for details in plan_jsons if details['plan_name'] in income_plans]
        age_plans = age_check(age_group,income_plan_details) 
        # plan=plans_age
        age_plan_details=[details for details in plan_jsons if details['plan_name'] in age_plans]
        # Goal Filter
        plans_details_goal_filter=[details for details in age_plan_details if goal in details["goals"] or details["goals"][0]=="Na"]
        final_plans=[x['plan_name'] for x in plans_details_goal_filter]
        while True:
            check=''.join([plan_details['Plan_summary'][plans] for plans in final_plans])
            if len(SALES_Copilot.encoding_.encode(check))<=2500:
                print(len(SALES_Copilot.encoding_.encode(check)))
                break 
            else:
                random_index = random.randint(0, len(final_plans) - 1)
                final_plans.pop(random_index)

        data=plan_details['Plan_summary']
        input_query=""
        for plan in list(data.keys()):
            if plan in final_plans:
                input_query=input_query+plan+"\n"+data[plan]+"\n"    
        final_resp=overall_chain({
            "age_group":age_group,
            "income_group":income_group,
            "goal":goal,
            "plan":final_plans,
            "input_query":input_query,
            "risk": risk,
            "example_learn":example_learn,
            "profile":profile
        })
        return final_resp
    
    @staticmethod
    def pitchgeneration(age_group,income_group,goal,tone,language_complexity,profile,emotional_appeal,example,template,beautify_template,plan_name,key_selling_point,model,character_prompt_pitch):
        pitch_len = '150'
        check_na=sales_copilot.sales_pitch_dict(plan_name,goal,profile)    
        if check_na=="Na":
            message=f"The product {plan_name} is not recommended with the specified Goal- {goal} and Profile- {profile}. It is suggested to change the Goal and Profile for the specified product"
            return {'response': message}
        print(check_na)
        
        with open('ABSLI_Sales_pitch_data.json', encoding="utf8") as f1:
            expected_sales_pitch_data = json.load(f1)
                
            plan_key = (goal+profile).replace(' ','')
            plan = [
                        "ABSLI Nischit Aayush Plan",
                        "ABSLI Assured Income Plus Plan",
                        "ABSLI Assured Savings Plan"
                        ]
            plan_contexts=""
            for key in plan:
                if plan_key in expected_sales_pitch_data[key]:
                                # if plan_name == "ABSLI Nischit Aayush Plan":
                    plan_contexts=plan_contexts+expected_sales_pitch_data[key][plan_key]+'\n'
                else:
                    plan_contexts=plan_contexts
            if plan_contexts =="":
                plan_contexts = "Consider key features to generate Sales Pitch"

            def get_completion(plan_name,key_features,plan_contexts,goal, profile,age_group, income_group,emotional_appeal,language_complexity,key_selling_point,tone):
                messages=[
                    {"role": "system", "content": "Your goal is to generate the Sales Pitch based on all parameters"},
                    {"role":"user","content":f"If goal is {goal} and profile is {profile} then generated sales Pich based on Key features, age group and income is?"},
                    {"role":"assistant","content":f""""{plan_contexts}"""},
                    {"role": "user", "content": f"These are details of the Customer i.e., emotion of cusomer is {emotional_appeal}, tone is {tone}, key selling points is {key_selling_point}, language complexity is {language_complexity} ,plan_name is {plan_name}, goal is {goal}, profile is {profile} then generate the sales pitch by mentioning the needs of customer with respect to their age and income which targets the age {age_group}, income {income_group} and goal{goal} based on  keyfeatures is {key_features}, age_group is {age_group}, income is {income_group}"}
                ]

                response = openai.ChatCompletion.create(
                    engine = "Absligpt35-SC",
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0,# this is the degree of randomness of the model's output
                )
                return response

            key_features = expected_sales_pitch_data[plan_name]["Key_features"]
            print(key_features)
            response = get_completion(plan_name, key_features,plan_contexts,goal, profile,age_group, income_group,emotional_appeal,language_complexity,key_selling_point,tone)
            example_learn = "Hello, and greetings to you, our valued customer! As a retired individual looking for a reliable insurance plan, the ABSLI Nischit Aayush Plan could be the perfect fit for you. With a minimum age entry of just 30 days, and a maximum age entry of 55 years, this plan is suitable for people like you who fall within this age bracket. Additionally, with a minimum premium amount of just Rs. 30,000 per annum, this plan is also ideal for individuals earning between 3-4 lakhs per year.Moreover, we understand that your goal is Retirement Planning, and the ABSLI Nischit Aayush Plan offers just that.Here are some of the key features makes you chose this plan as your perfect choice:\n1.You can choose to receive your income benefit in annual, semi-annual, quarterly or monthly frequency as per your convenience. \n2. With high language complexity and informative tone catering to your needs, the ABSLI Nischit Aayush Plan also offers an emotional appeal \n3. You can create a second source of income to manage your expenses and combat inflation while having a sense of financial security. \n4. You can also gift your children a guaranteed gift on their every birthday/marriage anniversary for the next 30 to 40 years followed by a guaranteed and tax-free lumpsum at maturity as a grand gift to them. \n5. We have several benifit options like death benifits, survival benifits, maturity benifits which secure your family with or without your presence. \nFinally, ABSLI Nischit Aayush Plan has many benefits that match your profile and goals. Please consider investing in this plan for an encumbrance-free asset for your loved ones. Thank you for giving us the opportunity to serve you."
            beautify_template="As a sales representative of an insurance company, you need to beautify a sales pitch {sales_pitch}.Limit the response to 200-250 words.Generate the sales pitch with some beautification that means highlight the benifits of plan with bullet points like 1,2,3,etc.,.Then only generate the sales pitch.\n Take this as an example: \n,{example_learn}\n your task is to make sure that the each response should be the same structure as the example provided."
            chain_review_beautify = LLMChain(llm=model, prompt=PromptTemplate.from_template(template=beautify_template), output_key="sale_pitch_beautify")

            overall_chain = SequentialChain(
                chains=[chain_review_beautify],
                input_variables=["sales_pitch","example_learn"],
                output_variables=["sale_pitch_beautify"],
            )
            sales_pitch = response["choices"][0]["message"]["content"]
            final_resp = overall_chain({
                        "sales_pitch": sales_pitch,
                        "example_learn": example_learn
                    })
            final_response = final_resp["sale_pitch_beautify"]
                    
            return final_response

    
    @staticmethod
    def num_tokens_from_messages_docs(messages: str) -> int:
        """
        Calculate the number of tokens in the given messages using the specified encoding.

        Args:
            messages (str): The input messages.
            encoding (str): The encoding type used to tokenize the messages.

        Returns:
            num_tokens (int): The total number of tokens in the messages.
            
        """

        num_tokens = 2
        for message in messages:
            num_tokens += (4 + len(SALES_Copilot.encoding_.encode(message)) + 1) # every message follows <im_start>{role/name}\n{content}<im_end>\n
            # num_tokens += len(encoding.encode(message)) + 1 # 1 is added to take into consideration the role
        # num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    @staticmethod
    def history_context(query:str,user_history:str,history_context_prompt:str) -> str:
        '''
        Generate a contextual prompt based on the user's query and history.

        Parameters:
            query (str): The user's current query or input.
            user_history (str): The user's previous interaction or conversation history.

        Returns:
            prompt (str): The contextual prompt generated based on the query and user history
        
        '''
        
        return f'''{history_context_prompt}
        Chat history:
        {user_history}

        Given question: {query}
        Rephrased question: 
        '''
    @staticmethod
    def generate_response(prompt: str) -> str:
        """
        Generate a response or text based on the given prompt using GPT.

        Parameters:
            prompt (str): The prompt or starting text for generating the response.
            
        Returns:
            response (str): The generated response based on the provided prompt.

        """

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["<|im_end|>", "<|im_start|>"]
        )
        return response['choices'][0]["text"]

    def multi_qa(user_query: str,model) -> str:
        """
        Generate a response based on context  using GPT.

        Parameters:
            user_query (str): Processed query entered by user
            
        Returns:
            response (str): The generated response based on the provided context.

        """
        
        prompt_template = """You are a helpful assistant who has to answer the question based on context.\
        If the question is not related to text check if its related to insruance if yes answer from your\
         knowledge base saying As per my intelligence... else simply respond "Don't know.\
         Make sure to give only relevant recommendations.

        {context}

        Question: {question}
        Answer here:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # model_name = 'gpt-3.5-turbo'
        # temperature = 0.0
        # model = OpenAI(model_name = model_name,engine="Absligpt35-SC",n=1,verbose=True,api_version="2023-03-15-preview",api_base="https://openaiabsli-sc.openai.azure.com/",api_key = openai.api_key,api_type="Azure")
        
        try:
            qa = RetrievalQA.from_chain_type(llm=model,
                                            chain_type="stuff",
                                            retriever=embeddings_plan1.as_retriever(top_k = 5),
                                            chain_type_kwargs={"prompt": PROMPT})
            result = qa.run(user_query)
            print(result)
            return result
        except Exception as e:

            return f' error occured in RetrievalQA {e}'


    @staticmethod
    def qa_driver(query: str,history:str,history_context_prompt:str,model):
        '''
        Generate an answer to a query based on a given history of interactions.

        Args:
            query (str): The input query or question.
            history (str): The history of interactions or conversation context.

        Returns:
            result (str): The generated answer to the query based on the provided history.
            search_query (str): The rephrased question.
    
        '''
        try:
            search_prompt = SALES_Copilot.history_context(query,history,history_context_prompt)
            search_query = SALES_Copilot.generate_response(search_prompt)
            print('Re-phrased Question:',search_query)
            result = SALES_Copilot.multi_qa(search_query)
            return result,search_query
        except Exception as e:
            return e
        

    @staticmethod    
    def sales_pitch_dict(product_name,goal,profile):

        '''
        Get a sales pitch based on the specified value, goal, and profile.
        
        Args:         
            product_name (str): The product name for which the sales pitch is requested.
            goal (str): The specific goal or context for the sales pitch.
            profile (str): The user's profile or preferences for customization.

        Returns:
            final_pitch (str): The generated sales pitch for the specified product_name, goal, and profile.

        '''
        product_mapping={"ABSLI Nischit Aayush Plan":"NAP","ABSLI Assured Income Plus Plan":"AIP","ABSLI Assured Savings Plan":"ASP",
            "ABSLI Poorna Suraksha":"Poorna Suraksha","ABSLI Digishield":"Digishield","ABSLI Saral Pension":"Saral Pension",
            "ABSLI Akshaya Plan":"Akshaya Plan","ABSLI Wealth Infinia":"Wealth Infinia","ABSLI Vision LifeIncome Plus Plan":"VLIP",
            "ABSLI Garanteed Annuity Plus":"GAP","ABSLI Nishchit Pension Plan":"NPP","ABSLI Fortune Elite Plan":"Fortune Elite",
            "ABSLI Cancer Shield Plan":"Cancer Shield Plan","ABSLI Wealth Secure Plan":"Wealth Secure Plan","ABSLI Guaranteed Milestone Plan":"GMS","ABSLI Child's Future Assured Plan":"CFAP",
            "ABSLI SecurePlus Plan":"SP","ABSLI Fixed Maturity Plan":"FMP","ABSLI Wealth Aspire Plan":"Wealth Aspire Plan",
            "ABSLI Wealth Assure Plus":"Wealth Assure Plan","ABSLI Vision LifeIncome Plan":"vLI",
            "ABSLI Nishchit Laabh":"NLP","ABSLI Wealth Max Plan":"WMP","ABSLI Critishield Plan":"CP","ABSLI Vision Endowment Plus Plan":"VEPP","ABSLI Assured FlexiSavings Plan":"AFSP"}
        
        if product_name not in list(product_mapping.keys()):
            return
        
        data=pd.read_excel('ABSLI_Sales_Pitch_Profile_Goals.xlsx',sheet_name=None,index_col=[1])
        pitch_data = data.get(product_mapping[product_name])
        pitch_data=pitch_data.iloc[:,1:]
        header_row = pitch_data.iloc[1]
        pitch_data.columns = header_row
        pitch_data.drop([pitch_data.index[0],pitch_data.index[1]],inplace = True)
        final_pitch=pitch_data[goal][profile]       
        return final_pitch
sales_copilot = SALES_Copilot()