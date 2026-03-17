"""
File: app.py
Date: June 21, 2023

This file contains a Flask application for sales pitch generation, recommendation, summarization and document question answering,

Description:
The main features of this application include:
- Sales pitch generation: The application offers endpoints for generating sales pitches based on customer's details and plan choosen.

- Recommendation: The application provides endpoints for recommendation of insurance plans based on customer details.

- Summarization: The application provides endpoints for summarization of sales pitches to generate pointers.

- Document question answering: The application provides endpoints for question and answering based on documents of the insurance plans.


Endpoints:
- /pitchgen [GET, POST]: Generating sales pitches.
- /recommendation [GET, POST]: Recommends insurance plans
- /summarization [GET, POST]: Creates summary for sales pitches.
- /doc_qa [GET, POST]: Performes question answering on documents.
- /chat [POST]: Identifies indent based on input query.

- dev routes- changes in the development requirements 

"""

from src.dependencies import *
from src.utils import *

tokenizer = tiktoken.get_encoding('cl100k_base')

history ={}
docs_history={}

llm = AzureChatOpenAI(
    deployment_name=deployment_id,
    temperature=0.0,

)
qa_llm = AzureOpenAI(deployment_name='dev',temperature=0)

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)


@app.route("/", methods=("GET", "POST"))
def home():
    return "Home Page"

@app.route('/chat', methods=['POST'])
def chat_api():
    global history
    global messages
    data = request.get_json()
    query = data['query']
    session_id = data['session_id']
    # array of string as questions

    response = qa_chat(query, session_id,history)
    return {"response":response}

@app.route("/pitchgen", methods=("GET", "POST"))
def pitch():
    if request.method == 'GET':
        return "Please make POST request on this route."
    
    elif request.method == 'POST':
        try:
            global pitch_gen
            plan_name = request.form['plan_names']
            age_group = request.form['age_group']
            goal = request.form['goal']
            income_group = request.form['income_group']
            # pitch_len = '200'
            profile = request.form['profile']
            tone = request.form['tone']
            key_selling_point = request.form['KSP']
            language_complexity = request.form['language_complexity']
            emotional_appeal = request.form['emotional_appeal']
            
            final_response = sales_copilot.pitchgeneration(age_group,income_group,goal,tone,language_complexity,profile,emotional_appeal,example,template,beautify_template,plan_name,key_selling_point,model,character_prompt_pitch)
                    
            return {'response': final_response}
        except Exception as e:
            return {'response': f"Error {e} occurred."}
        
@app.route("/summarization", methods=("GET", "POST"))

def summarization():
    if request.method == 'GET':
        return "Please send POST Request on this route"
    elif request.method == 'POST':
        try:
            pitch_gen = request.form['pitch_gen']
            summarize_content = sales_copilot.summarize(pitch_gen)
            summarize_content = summarize_content.replace("<|im_end|>", "") if "<|im_end|>" in summarize_content  else summarize_content
            return {'response': summarize_content}
        except Exception as e:
             return {"response":f'Error {e} occured.'}
            

@app.route("/recommendhindi", methods=("GET", "POST"))
def pitchhindirecommend():
    if request.method == 'GET':
        return "Please make POST request on this route."
    
    elif request.method == 'POST':
        try:
            hindi_recommendation = request.form['recommendation']
            body = [{
                'text': hindi_recommendation
                    }]
            request_n = requests.post(constructed_url, params=params, headers=headers, json=body)
            response_n = request_n.json()
            return {'response': response_n[0]["translations"][0]["text"]}
        except Exception as e:
            return {"response":f'Error {e} occured.'}

@app.route("/recommendation", methods=("GET", "POST"))
def recommend():
    if request.method == 'GET':
        return "Please make POST request on this route."
    elif request.method == 'POST':
        try:
            age_group = request.form['age_group']
            goal = request.form['goal']
            income_group = request.form['income_group']
            risk = request.form['risk']
            profile = request.form['profile']
            # Calling the function
            final_resp = sales_copilot.recommendation(age_group,goal,income_group,risk,profile,example_recommend,model,recommend_template)
            return {'response': str(final_resp['Recommend_pitch'])}
        except Exception as e:
             return {"response":f'Error {e} occured.'}
        
@app.route("/pitchgenhindi", methods=("GET", "POST"))
def pitchhindi():
    
    if request.method == 'GET':
        return "Please make POST request on this route."
    
    elif request.method == 'POST':
        sales_pitch = request.form['sales_pitch']
        body = [{
            'text': sales_pitch
            }]
        request_n = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_n = request_n.json()
        
        return {'response': response_n[0]["translations"][0]["text"]}
    
@app.route('/dev/chat', methods=['POST'])
def dev_chat_api():
    data = request.get_json()
    query = data['query']
    history = data['history']
    # array of string as questions
    
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
        try:
            res,search_query = sales_copilot.qa_driver(query,history,history_context_prompt,model)
            response = {'response': {'question':str(search_query),'answer':str(res)}}
            print(res)
            return response
        except Exception as e:
            return {'response': f"Error {e} occured."}
        

@app.route("/dev/pitchgen", methods=("GET", "POST"))
def dev_pitch():
    if request.method == 'GET':
        return "Please make POST request on this route."
    elif request.method == 'POST':
        try:
            global pitch_gen
            plan_name = request.form['plan_names']
            age_group = request.form['age_group']
            goal = request.form['goal']
            income_group = request.form['income_group']
            pitch_len = '200'
            profile = request.form['profile']
            tone = request.form['tone']
            key_selling_point = request.form['KSP']
            language_complexity = request.form['language_complexity']
            emotional_appeal = request.form['emotional_appeal']
            
            f1 = open('ABSLI_Sales_pitch_data.json', encoding="utf8")
            NAP_data = json.load(f1)
            #print(NAP_data)
           
            # This is an LLMChain( Sequential chain).
            
            plan_key = goal+profile
            plan_key = plan_key.replace(' ','')
            e_data=""
            plan = [
                "ABSLI Nischit Aayush Plan",
                "ABSLI Assured Income Plus Plan", 
                "ABSLI Assured Savings Plan"
                ]
            for key in plan:
                try:
                    e_data=e_data+NAP_data[key][plan_key]+'\n'
                    json_data = "Following are the plan details:"+plan_name+e_data+'\n'+"Please consider the key features of the plan mentioned here: "+NAP_data[plan_name]['Key_features']+" Following are the parameters to consider while generating sales pitch: length of the pitch: "+pitch_len+" words, tone: "+tone+", key selling points: "+key_selling_point+", language complexity: "+language_complexity+", emotional appeal: "+emotional_appeal+"USE ONLY RELEVANT CONVERSATION STARTERS IN THE BEGINNING BASED UPON CUSTOMER'S GOAL."
                    print("JSON Data",json_data)     
                    if json_data != "NA":                
                        context = json_data
                   
                    print(context)             
                except:
                    continue
                
                character_prompt_pitch = "You are a sales representative for Aditya Birla Sun Life Insurance (ABSLI), \
                a leading insurance company. Your goal is to create a sales pitch for an ABSLI product,\
                taking into account their age group, annual income, and goal."
                
                prompt_tokens01 = len(encoding.encode(character_prompt_pitch))
                
                prompt_tokens02 = len(encoding.encode(context))
                
                prompt_token = prompt_tokens01 + prompt_tokens02
                
                if(prompt_token >= token_limit):
                    return {'response' :f'Max token limit reached. You used {prompt_token} tokens.'}
                
                elif(prompt_token + int(pitch_len) >= token_limit):
                    return {'response' :f'Generating this answer would cause the token limit to be breached and may generate partial answers. You used {prompt_token+int(pitch_len)} tokens.'}
                
                prompt_review = PromptTemplate.from_template(
                    template=template
                )
                chain_review = LLMChain(llm=model, prompt=prompt_review, output_key="sales_pitch")
                
                prompt_final=PromptTemplate.from_template(
                    template=beautify_template
                )
                chain_review_beautify = LLMChain(llm=model, prompt=prompt_final, output_key="sale_pitch_beautify")
                overall_chain = SequentialChain(
                            chains=[chain_review,chain_review_beautify],
                            input_variables=["age_group","income_group","goal","pitch_len","tone","language_complexity","emotional_appeal",
                                             "plan_name","context","profile","example_learn"],
                            output_variables=["sales_pitch","sale_pitch_beautify"],
                    )
                example_learn =  example          
                final_resp =overall_chain({"age_group":age_group,"income_group":income_group,"goal":goal,"pitch_len":pitch_len,"tone":tone,
                                          "language_complexity":language_complexity,"emotional_appeal":emotional_appeal,"plan_name":plan_name,"context":context,"profile": profile,"example_learn":example_learn})
                final_response = final_resp["sale_pitch_beautify"]

                    
                return {'response': final_response}
            else:
                return {'response': "I apologize, but it appears that this particular plan may not be the best fit for your specific goals.\
                May I suggest considering an alternative plan(ABSLI Assured Income Plus/ABSLI Assured Savings Plan) \
                that may better align with your needs."}
        except  Exception as e:
            return {'response': f"Error {e} occured."}

@app.route("/dev/summarization", methods=("GET", "POST"))
def dev_summarization():
    
    if request.method == 'GET':
        return "Please send POST Request on this route"
    
    elif request.method == 'POST':
        try:
            pitch_gen = request.form['pitch_gen']
            summarize_content = sales_copilot.summarize(pitch_gen)
            return {'response': summarize_content}
        except Exception as e:
             return {"response":f'Error {e} occured.'}

@app.route("/dev/recommendhindi", methods=("GET", "POST"))
def dev_pitchhindirecommend():
    if request.method == 'GET':
        return "Please make POST request on this route."
    
    elif request.method == 'POST':
        try:
            hindi_recommendation = request.form['recommendation']
            body = [{
                'text': hindi_recommendation
                    }]
            request_n = requests.post(constructed_url, params=params, headers=headers, json=body)
            response_n = request_n.json()
            return {'response': response_n}
        except Exception as e:
            return {"response":f'Error {e} occured.'}

@app.route("/dev/recommendation", methods=("GET", "POST"))
def dev_recommend():
    if request.method == 'GET':
        return "Please make POST request on this route."
    elif request.method == 'POST':
        try:
            age_group = request.form['age_group']
            goal = request.form['goal']
            income_group = request.form['income_group']
            risk = request.form['risk']

            ##Extracting Summary from Blob storage
            blob_client = container_client.get_blob_client('ABSLI_recommendation_summary.json')
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
            input_variables=["age_group","income_group","goal","plan","input_query","risk","example_learn"],
            output_variables=["Recommend_pitch"],
                )
            
            income_plans = income_check(income_group,plan_jsons)
            plan_extracted=[value for value in plan_jsons if value['plan_name'] in income_plans]
            plans_age = age_check(age_group,plan_extracted)
            try:
                plans_age=random.sample(plans_age,k=4)
            except:
                pass 
            plan=plans_age

            data=plan_details['Plan_summary']
            input_query=""
            for i in list(data.keys()):
                if i in plan:
                    input_query=input_query+i+"\n"+data[i]+"\n"    
            final_resp=overall_chain({"age_group":age_group,"income_group":income_group,"goal":goal,"plan":plan,"input_query":input_query,"risk": risk,"example_learn":example_learn})          

            return {'response': str(final_resp['Recommend_pitch'])}
        except Exception as e:
             return {"response":f'Error {e} occured.'}

        
@app.route("/dev/pitchgenhindi", methods=("GET", "POST"))
def dev_pitchhindi():
    
    if request.method == 'GET':
        return "Please make POST request on this route."
    
    elif request.method == 'POST':
        sales_pitch = request.form['sales_pitch']
        body = [{
            'text': sales_pitch
            }]
        request_n = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_n = request_n.json()
        
        return {'response': response_n[0]["translations"][0]["text"]}

if __name__ == '__main__':
    app.run(debug = True,use_reloader=False)