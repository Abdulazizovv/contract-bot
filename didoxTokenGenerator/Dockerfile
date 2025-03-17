# Use the official OpenJDK 21 image as the base
FROM eclipse-temurin:21-jdk

# Set the working directory inside the container
WORKDIR /app

# Copy the main application JAR to the working directory
COPY TokenGenerator-1.0-SNAPSHOT.jar /app/TokenGenerator-1.0-SNAPSHOT.jar

# Copy the dependencies in the lib directory to the working directory
COPY lib /app/lib
COPY keys /app/keys

# Expose the port your Spring Boot application uses
EXPOSE 8080

# Command to run the application
CMD ["java", "-cp", "TokenGenerator-1.0-SNAPSHOT.jar:lib/*", "org.springframework.boot.loader.JarLauncher"]

