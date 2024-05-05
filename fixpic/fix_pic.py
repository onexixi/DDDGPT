from gradio_client import Client

client = Client("https://hahahe-gfpgan-fix.hf.space/",hf_token='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')
result = client.predict(
				"C:\\Users\\Administrator\\Pictures\\5b3f647b-6298-4f7f-bc19-a03bbc4a019e.png",	# str representing filepath or URL to image in 'Input' Image component
				"v1.2",	# str representing string value in 'version' Radio component
				5,	# int | float representing numeric value in 'Rescaling factor' Number component
				api_name="/predict"
)
result[0]
result[1]
print(result)
