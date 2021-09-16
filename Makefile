container:
	cd frontend; yarn build
	docker build -t zctaimpacts .
push-container:
	docker tag zctaimpacts abriedev/zctaimpacts:latest
	docker push abriedev/zctaimpacts:latest
run-container:
	docker run -p 5000:5000 -v $(PWD)/backend/instance:/backend/instance -v $(PWD)/frontend/build:/backend/app/static zctaimpacts

