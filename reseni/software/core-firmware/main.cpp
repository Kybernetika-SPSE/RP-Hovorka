#include <chrono>
#include <iostream>
#include <optional>
#include <string>
#include <thread>
#include <vector>

namespace camera_project {

enum class Mode {
    Preview,
    Menu,
    Capture,
    Playback,
    Sleep,
    Error,
};

struct Settings {
    int iso = 200;
    double aperture = 2.8;
    int shutterSpeedUs = 10000;
    bool liveViewEnabled = true;
};

struct Frame {
    int width = 0;
    int height = 0;
    std::vector<unsigned char> data;
};

class Camera {
public:
    bool initialize() {
        std::cout << "[camera] initialize\n";
        return true;
    }

    std::optional<Frame> captureFrame() {
        std::cout << "[camera] capture frame\n";
        Frame frame;
        frame.width = 640;
        frame.height = 480;
        frame.data.resize(static_cast<std::size_t>(frame.width * frame.height));
        return frame;
    }
};

class Display {
public:
    bool initialize() {
        std::cout << "[display] initialize\n";
        return true;
    }

    void showStatus(const std::string& text) {
        std::cout << "[display] " << text << '\n';
    }

    void showFrame(const Frame& frame) {
        std::cout << "[display] show frame " << frame.width << "x" << frame.height << '\n';
    }
};

class Storage {
public:
    bool initialize() {
        std::cout << "[storage] initialize\n";
        return true;
    }

    bool saveFrame(const Frame& frame, const std::string& fileName) {
        std::cout << "[storage] save " << fileName << " (" << frame.width << "x" << frame.height << ")\n";
        return true;
    }
};

class EfMount {
public:
    bool initialize() {
        std::cout << "[ef] initialize\n";
        return true;
    }

    bool applySettings(const Settings& settings) {
        std::cout << "[ef] iso=" << settings.iso
                  << " aperture=" << settings.aperture
                  << " shutter_us=" << settings.shutterSpeedUs << '\n';
        return true;
    }
};

class PowerManager {
public:
    void enterSleep() {
        std::cout << "[power] sleep\n";
    }
};

class CoreFirmware {
public:
    bool initialize() {
        if (!camera_.initialize()) return false;
        if (!display_.initialize()) return false;
        if (!storage_.initialize()) return false;
        if (!efMount_.initialize()) return false;

        display_.showStatus("Core firmware ready");
        return true;
    }

    void runDemoLoop() {
        display_.showStatus("preview mode");
        for (int iteration = 0; iteration < 3; ++iteration) {
            tick();
        }

        settings_.iso = 400;
        settings_.shutterSpeedUs = 8000;
        efMount_.applySettings(settings_);

        mode_ = Mode::Capture;
        capturePhoto();

        mode_ = Mode::Sleep;
        power_.enterSleep();
    }

private:
    void tick() {
        if (mode_ != Mode::Preview || !settings_.liveViewEnabled) {
            return;
        }

        auto frame = camera_.captureFrame();
        if (frame.has_value()) {
            display_.showFrame(*frame);
        }
    }

    void capturePhoto() {
        auto frame = camera_.captureFrame();
        if (!frame.has_value()) {
            mode_ = Mode::Error;
            display_.showStatus("capture failed");
            return;
        }

        if (storage_.saveFrame(*frame, "IMG_0001.raw")) {
            display_.showStatus("photo saved");
            mode_ = Mode::Preview;
        } else {
            mode_ = Mode::Error;
            display_.showStatus("save failed");
        }
    }

    Mode mode_ = Mode::Preview;
    Settings settings_{};
    Camera camera_{};
    Display display_{};
    Storage storage_{};
    EfMount efMount_{};
    PowerManager power_{};
};

}  // namespace camera_project

int main() {
    camera_project::CoreFirmware firmware;
    if (!firmware.initialize()) {
        std::cerr << "Core firmware init failed\n";
        return 1;
    }

    firmware.runDemoLoop();
    return 0;
}
