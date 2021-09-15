container:
	docker build -t sustainable .
run-container:
	docker run -p 5000:5000 -v $(PWD)/backend/instance:/backend/instance -v $(PWD)/frontend/build:/backend/app/static sustainable

