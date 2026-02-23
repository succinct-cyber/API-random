Single Task Operations — The Detail View
So far our API can:

- GET all tasks
- POST a new task

The URL Structure
First, understand how we identify a single object in an API. We pass the ID directly in the URL:


get_object_or_404(Task, pk=pk) — This is a Django shortcut. It tries to find a Task with the given pk. If it exists, it returns it. If it doesn't exist, it automatically returns a 404 Not Found response. Clean and safe.

get_object(self, pk) — We defined this as a helper method on the class so we don't repeat the same fetch logic in every method. Every HTTP method (GET, PUT, PATCH, DELETE) needs to first fetch the task — so we centralize that in one place.

TaskSerializer(task) — Notice here we pass the task instance directly (no data= keyword). This means we're serializing — converting the object to JSON for output.

TaskSerializer(task, data=request.data) — Here we pass both the existing task instance AND the new incoming data. This tells the serializer "update this existing object with this new data."

partial=True in PATCH — This is the key difference between PUT and PATCH. Without partial=True, the serializer expects all fields to be provided. With partial=True, it's fine with receiving just one or two fields — perfect for something like just toggling completed to true.

HTTP_204_NO_CONTENT — The standard status code for a successful DELETE. It means "it worked, and there's nothing to send back."

<int:pk> — This is a URL parameter. It captures whatever integer is in that position of the URL and passes it as pk to the view. So when someone hits /api/tasks/3/, Django extracts 3 and passes it as pk=3 to the view methods.

