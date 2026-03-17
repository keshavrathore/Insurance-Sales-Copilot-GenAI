# Replace the placeholders with your Azure Blob Storage account details
account_name = 'storageaccabslichatgpt01'
account_key = 'abcds+ASte521fg=='
container_name = 'metadata'

# Create a connection string using the account name and account key
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

#Azure gpt-turbo openai credentials
OPENAI_API_KEY = "abcds"
API_TYPE = "azure"
API_BASE = "https://openaiabsli-sc.openai.azure.com/"
API_VERSION = "2023-03-15-preview"

# endpoint for form recognizer
FR_ENDPOINT = "https://formrecognizer-absli-chatgpt-01.cognitiveservices.azure.com/"

# key for form recognizer
FR_KEY = "ef3182b11c5f44e8bac53f55322c7ca2"

# cosmosDB end points
DB_ENDPOINT = "https://cosmosdb-absli-chatgpt-01.documents.azure.com:443/"
DB_KEY = "abcds=="
DB_NAME = 'extracted_data'
DB_CONTAINER = 'Embeddings'

# faiss_indexer_path
faiss_index = "faiss_index/"

# translator end points 
key = "6dec3bf4be3d453faced3641311e75bd"
endpoint = "https://api.cognitive.microsofttranslator.com"
path = '/translate'

constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['hi']
}

location = "centralindia"

# sales pitch template
template="As a sales representative of an insurance company, you need to generate a sales pitch by taking into account the customer's entry age group{age_group}, income{income_group}, goals{goal}, profile{profile},pitch length{pitch_len},tone of customer{tone},language complexity{language_complexity} and emotional appeal{emotional_appeal}. Compare the customer's details with the plan details of {plan_name} and its context {context}, as well as the plan's eligibility criteria.For example, you are speaking with a customer who is xxx old at the entry of plan. The plan you are discussing has a minimum age entry of x year and a maximum age entry of xx years. In your sales pitch, mention that people below the age of maximum entry age of the plan and above the minimum entry age of the plan mentioned in plan details are perfect for this plan, while those above that age may want to consider another plan.Example2 is If the income is 2 lakhs and the plan minimum premium amount is 30000 then we mention it is pefect plan based on income of customer.Take the previous examples as a sample ones and perform based on the context provided for that plan.Mention the benefits of this plan to make the customer purchase our plan by explaining the matches between customer's deatils and plans eligibility criteria. Start the conversation by greeting the customer in a very friendly manner based on their profile {profile}.Limit the response to 200-250 words.Then, generate the sales pitch."

#sales beautification template
beautify_template="As a sales representative of an insurance company, you need to generate a sales pitch by taking into account the customer's entry age group{age_group}, income{income_group}, goals{goal}, profile{profile},pitch length{pitch_len},tone of customer{tone},language complexity{language_complexity} and emotional appeal{emotional_appeal}. Compare the customer's details with the plan details of {plan_name} and its context {context}, as well as the plan's eligibility criteria.For example, you are speaking with a customer who is xxx old at the entry of plan. The plan you are discussing has a minimum age entry of x year and a maximum age entry of xx years. In your sales pitch, mention that people below the age of maximum entry age of the plan and above the minimum entry age of the plan mentioned in plan details are perfect for this plan, while those above that age may want to consider another plan.Example2 is If the income is 2 lakhs and the plan minimum premium amount is 30000 then we mention it is pefect plan based on income of customer.Take the previous examples as a sample ones and perform based on the context provided for that plan.Mention the benefits of this plan to make the customer purchase our plan by explaining the matches between customer's deatils and plans eligibility criteria. Start the conversation by greeting the customer in a very friendly manner based on their profile {profile}.Limit the response to 200-250 words.Generate the sales pitch with some beautification that means highlight the benifits of plan with bullet points like 1,2,3,etc.,.Then only generate the sales pitch.\n Take this as an example: \n,{example_learn}\n your task is to make sure that the each response should be the same structure as the example provided."

# sales_pitch example
example =  "Hello, and greetings to you, our valued customer! As a retired individual looking for a reliable insurance plan, the ABSLI Nischit Aayush Plan could be the perfect fit for you. With a minimum age entry of just 30 days, and a maximum age entry of 55 years, this plan is suitable for people like you who fall within this age bracket. Additionally, with a minimum premium amount of just Rs. 30,000 per annum, this plan is also ideal for individuals earning between 3-4 lakhs per year.Moreover, we understand that your goal is Retirement Planning, and the ABSLI Nischit Aayush Plan offers just that.Here are some of the key features makes you chose this plan as your perfect choice:\n1.You can choose to receive your income benefit in annual, semi-annual, quarterly or monthly frequency as per your convenience. \n2. With high language complexity and informative tone catering to your needs, the ABSLI Nischit Aayush Plan also offers an emotional appeal \n3. You can create a second source of income to manage your expenses and combat inflation while having a sense of financial security. \n4. You can also gift your children a guaranteed gift on their every birthday/marriage anniversary for the next 30 to 40 years followed by a guaranteed and tax-free lumpsum at maturity as a grand gift to them. \n5. We have several benifit options like death benifits, survival benifits, maturity benifits which secure your family with or without your presence. \nFinally, ABSLI Nischit Aayush Plan has many benefits that match your profile and goals. Please consider investing in this plan for an encumbrance-free asset for your loved ones. Thank you for giving us the opportunity to serve you."

example_recommend = "Recommended Plan: ABSLI Assured Savings Plan\n\nReason: Hello! Thank you for enquiring about our plans. Based on your details, the ABSLI Assured Savings Plan would be a suitable option for you to achieve your goal of child marriage with moderate risk. Here are some reasons why we recommend this plan:\n 1- The plan provides a secure future with guaranteed lumpsum benefits upon policy maturity, ensuring financial stability at the time of marriage.\n 2- You have the flexibility to choose a policy term of up to 35 years, allowing you to plan for the long-term financial needs of your child.\n 3- The premium payment options available are Single pay and Limited pay, providing you with the flexibility to choose a premium payment option that suits your income.\n 4- The policy term options available are 5 years, 10 years, 15 years, 20 years, 25 years, 30 years, and 35 years, providing you with the flexibility to choose a term that aligns with your child's age at the time of the marriage.\n 5- The benefits of this plan include a death benefit of sum assured plus Accrued Loyalty Additions, a maturity benefit of lump sum payouts plus Accrued Loyalty Additions, and tax benefits on premiums paid and benefits received as per prevailing tax laws.\n\nWe hope you found our recommendation helpful. Let us know if you have any further questions or if you would like to proceed with this plan. Thank you for considering ABSLI."

character_prompt_pitch = "You are a sales representative for Aditya Birla Sun Life Insurance (ABSLI), a leading insurance company. Your goal is to create a sales pitch for an ABSLI product, taking into account their age group, annual income, and goal."
